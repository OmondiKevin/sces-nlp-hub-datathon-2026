#!/usr/bin/env python3
"""Fine-tune a joint intent and slot model for the Strathmore NLP Datathon.

The CSV's existing ``train``, ``validation`` and ``test`` assignments are
preserved. Intent labels are read from the handbook's ``label`` column (or the
legacy ``label(intent)`` alias); slot spans are read from ``slots_json``. Slot labels are projected onto whitespace-delimited
words, then aligned to the first tokenizer sub-token for each word; special
tokens, padding and remaining sub-tokens receive the cross-entropy ignore
index (-100).

AfriBERTa large is the default backbone because it is pretrained on Swahili
and other African languages and is practical to fine-tune on a Colab T4. The
model card recommends setting its tokenizer maximum length explicitly, which
this script does.

Install dependencies (choose the PyTorch build appropriate for your CUDA):
    pip install -r requirements-model.txt

Example:
    python train_joint_intent_slot.py \
        --data Team_22_Dataset_Track_C.csv \
        --output-dir outputs/joint_afriberta \
        --epochs 8 --batch-size 8 --gradient-accumulation-steps 2 \
        --use-crf --augment-slot-values

The default is the historical CRF plus conservative training-only slot-value
substitution configuration. It is a candidate, not an assumed winner on the
final split. Compare it with validation-only ablations before the one test run.
Substitutions use the same intent, slot type and word count; original rows are
always retained. Use ``--no-crf --no-slot-value-augmentation`` for the
independent-token, no-augmentation ablation.

The script saves the best validation checkpoint, tokenizer, label mappings,
Track C metrics and predictions, a run manifest, and up to five actual errors.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import random
import re
from collections import defaultdict
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoModel,
    AutoTokenizer,
    get_linear_schedule_with_warmup,
)

from track_c_evaluation import (
    bio_tags_to_char_slots,
    evaluate_track_c,
    load_track_c_rows,
    normalize_slot_value,
    validate_track_c_splits,
)


DEFAULT_MODEL_NAME = "castorini/afriberta_large"
IGNORE_INDEX = -100
VALID_SPLITS = ("train", "validation", "test")


@dataclass
class PreparedExample:
    """Tokenized model inputs plus metadata used for evaluation and reporting."""

    input_ids: list[int]
    attention_mask: list[int]
    slot_labels: list[int]
    first_subtoken_mask: list[int]
    intent_label: int
    text: str
    record_id: str
    words: list[str]
    word_labels: list[str]
    slot_annotations: list[dict[str, Any]]


class JointDataset(Dataset):
    def __init__(self, examples: list[PreparedExample]):
        self.examples = examples

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> PreparedExample:
        return self.examples[index]


class LinearChainCRF(nn.Module):
    """Linear-chain CRF with hard BIO transition constraints and Viterbi decode."""

    def __init__(self, labels: list[str]) -> None:
        super().__init__()
        self.labels = labels
        self.num_tags = len(labels)
        self.transitions = nn.Parameter(torch.empty(self.num_tags, self.num_tags))
        self.start_transitions = nn.Parameter(torch.empty(self.num_tags))
        self.end_transitions = nn.Parameter(torch.empty(self.num_tags))
        nn.init.uniform_(self.transitions, -0.1, 0.1)
        nn.init.uniform_(self.start_transitions, -0.1, 0.1)
        nn.init.uniform_(self.end_transitions, -0.1, 0.1)

        # A sequence may start with O/B, and I-X may only follow B-X or I-X.
        start_allowed = torch.tensor([not label.startswith("I-") for label in labels])
        transitions_allowed = torch.ones(self.num_tags, self.num_tags, dtype=torch.bool)
        for previous_id, previous in enumerate(labels):
            for current_id, current in enumerate(labels):
                if current.startswith("I-"):
                    current_type = current[2:]
                    transitions_allowed[previous_id, current_id] = previous in {
                        f"B-{current_type}",
                        f"I-{current_type}",
                    }
        self.register_buffer("start_allowed", start_allowed)
        self.register_buffer("transitions_allowed", transitions_allowed)

    def _constrained_scores(self) -> tuple[torch.Tensor, torch.Tensor]:
        transitions = self.transitions.masked_fill(~self.transitions_allowed, -10000.0)
        starts = self.start_transitions.masked_fill(~self.start_allowed, -10000.0)
        return transitions, starts

    def neg_log_likelihood(
        self,
        emissions: torch.Tensor,
        tags: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        if emissions.ndim != 3 or tags.shape != emissions.shape[:2] or mask.shape != tags.shape:
            raise ValueError("CRF expects emissions [batch, words, tags] and tags/mask [batch, words].")
        if not bool(mask[:, 0].all()):
            raise ValueError("Every CRF sequence must contain at least one word.")

        transitions, starts = self._constrained_scores()
        batch_ids = torch.arange(emissions.size(0), device=emissions.device)
        alpha = starts.unsqueeze(0) + emissions[:, 0]
        for timestep in range(1, emissions.size(1)):
            candidates = (
                alpha.unsqueeze(2)
                + transitions.unsqueeze(0)
                + emissions[:, timestep].unsqueeze(1)
            )
            next_alpha = torch.logsumexp(candidates, dim=1)
            alpha = torch.where(mask[:, timestep].unsqueeze(1), next_alpha, alpha)
        log_partition = torch.logsumexp(alpha + self.end_transitions.unsqueeze(0), dim=1)

        gold_score = starts[tags[:, 0]] + emissions[batch_ids, 0, tags[:, 0]]
        for timestep in range(1, emissions.size(1)):
            transition_score = transitions[tags[:, timestep - 1], tags[:, timestep]]
            emission_score = emissions[batch_ids, timestep, tags[:, timestep]]
            gold_score = gold_score + (transition_score + emission_score) * mask[:, timestep]
        last_indices = mask.long().sum(dim=1) - 1
        last_tags = tags[batch_ids, last_indices]
        gold_score = gold_score + self.end_transitions[last_tags]
        # Normalize per word so the CRF slot objective stays on a scale
        # comparable to the token-average cross-entropy baseline.
        sequence_lengths = mask.long().sum(dim=1).to(emissions.dtype)
        return ((log_partition - gold_score) / sequence_lengths).mean()

    @torch.no_grad()
    def decode(self, emissions: torch.Tensor, mask: torch.Tensor) -> list[list[int]]:
        transitions, starts = self._constrained_scores()
        paths: list[list[int]] = []
        for batch_index in range(emissions.size(0)):
            length = int(mask[batch_index].sum().item())
            score = starts + emissions[batch_index, 0]
            backpointers: list[torch.Tensor] = []
            for timestep in range(1, length):
                candidates = score.unsqueeze(1) + transitions
                best_score, best_previous = candidates.max(dim=0)
                score = best_score + emissions[batch_index, timestep]
                backpointers.append(best_previous)
            last_tag = int((score + self.end_transitions).argmax().item())
            path = [last_tag]
            for backpointer in reversed(backpointers):
                last_tag = int(backpointer[last_tag].item())
                path.append(last_tag)
            paths.append(list(reversed(path)))
        return paths


class JointTransformerModel(nn.Module):
    """Shared Transformer encoder with sentence- and token-level heads."""

    def __init__(
        self,
        model_name: str,
        num_intents: int,
        num_slot_labels: int,
        slot_label_names: list[str],
        dropout: float = 0.1,
        gradient_checkpointing: bool = True,
        use_crf: bool = False,
    ) -> None:
        super().__init__()
        # We pool from last_hidden_state[:, 0] ourselves, so do not create an
        # unused randomly initialized XLM-R/BERT pooler.
        self.encoder = AutoModel.from_pretrained(model_name, add_pooling_layer=False)
        hidden_size = getattr(self.encoder.config, "hidden_size", None)
        if hidden_size is None:
            hidden_size = getattr(self.encoder.config, "d_model", None)
        if hidden_size is None:
            raise ValueError("Could not determine the encoder hidden size from its config.")

        if gradient_checkpointing and hasattr(self.encoder, "gradient_checkpointing_enable"):
            self.encoder.gradient_checkpointing_enable()
            if hasattr(self.encoder.config, "use_cache"):
                self.encoder.config.use_cache = False

        self.dropout = nn.Dropout(dropout)
        self.intent_classifier = nn.Linear(hidden_size, num_intents)
        self.slot_classifier = nn.Linear(hidden_size, num_slot_labels)
        self.crf = LinearChainCRF(slot_label_names) if use_crf else None

    @staticmethod
    def _compact_word_sequences(
        slot_logits: torch.Tensor,
        first_subtoken_mask: torch.Tensor,
        slot_labels: Optional[torch.Tensor] = None,
    ) -> tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]:
        """Gather one emission per word and pad the resulting word sequences."""
        from torch.nn.utils.rnn import pad_sequence

        emission_sequences = [
            slot_logits[index, first_subtoken_mask[index]]
            for index in range(slot_logits.size(0))
        ]
        lengths = torch.tensor(
            [sequence.size(0) for sequence in emission_sequences],
            dtype=torch.long,
            device=slot_logits.device,
        )
        word_emissions = pad_sequence(emission_sequences, batch_first=True, padding_value=0.0)
        positions = torch.arange(word_emissions.size(1), device=slot_logits.device)
        word_mask = positions.unsqueeze(0) < lengths.unsqueeze(1)
        word_targets = None
        if slot_labels is not None:
            target_sequences = [
                slot_labels[index, first_subtoken_mask[index]]
                for index in range(slot_labels.size(0))
            ]
            word_targets = pad_sequence(target_sequences, batch_first=True, padding_value=0)
        return word_emissions, word_mask, word_targets

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        intent_labels: Optional[torch.Tensor] = None,
        slot_labels: Optional[torch.Tensor] = None,
        first_subtoken_mask: Optional[torch.Tensor] = None,
        slot_loss_weight: float = 1.0,
        decode_slots: bool = False,
    ) -> dict[str, Any]:
        encoder_output = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=True,
        )
        hidden_states = encoder_output.last_hidden_state

        # AfriBERTa/XLM-R place the sentence classification token at position 0.
        intent_logits = self.intent_classifier(self.dropout(hidden_states[:, 0]))
        slot_logits = self.slot_classifier(self.dropout(hidden_states))

        intent_loss = None
        slot_loss = None
        total_loss = None
        slot_predictions = None
        if intent_labels is not None:
            intent_loss = F.cross_entropy(intent_logits, intent_labels)
        if self.crf is not None:
            if first_subtoken_mask is None:
                raise ValueError("first_subtoken_mask is required when using the CRF slot head.")
            word_emissions, word_mask, word_targets = self._compact_word_sequences(
                slot_logits,
                first_subtoken_mask,
                slot_labels,
            )
            if word_targets is not None:
                slot_loss = self.crf.neg_log_likelihood(word_emissions, word_targets, word_mask)
            if decode_slots:
                slot_predictions = self.crf.decode(word_emissions, word_mask)
        elif slot_labels is not None:
            slot_loss = F.cross_entropy(
                slot_logits.reshape(-1, slot_logits.shape[-1]),
                slot_labels.reshape(-1),
                ignore_index=IGNORE_INDEX,
            )
        if intent_loss is not None and slot_loss is not None:
            total_loss = intent_loss + slot_loss_weight * slot_loss

        return {
            "loss": total_loss,
            "intent_loss": intent_loss,
            "slot_loss": slot_loss,
            "intent_logits": intent_logits,
            "slot_logits": slot_logits,
            "slot_predictions": slot_predictions,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train and evaluate a joint intent classification/slot filling model."
    )
    parser.add_argument("--data", type=Path, default=Path("Team_22_Dataset_Track_C.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/joint_afriberta"))
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--slot-loss-weight", type=float, default=1.0)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--early-stopping-patience", type=int, default=3)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--use-crf",
        action="store_true",
        default=True,
        help="Use a constrained BIO CRF over word-level slot emissions.",
    )
    parser.add_argument(
        "--no-crf",
        action="store_false",
        dest="use_crf",
        help="Disable the CRF to reproduce the independent-token baseline.",
    )
    parser.add_argument(
        "--augment-slot-values",
        action="store_true",
        default=True,
        help=(
            "Add one conservative training-only entity replacement per eligible row, "
            "matching intent, slot type and span word count."
        ),
    )
    parser.add_argument(
        "--no-slot-value-augmentation",
        action="store_false",
        dest="augment_slot_values",
        help="Disable synthetic slot-value swaps for the baseline.",
    )
    parser.add_argument(
        "--precision",
        choices=("auto", "fp16", "bf16", "no"),
        default="auto",
        help="Mixed precision mode. 'auto' uses BF16 when supported, otherwise FP16 on CUDA.",
    )
    parser.add_argument(
        "--expected-intents",
        type=int,
        default=10,
        help="Require this many intent labels (the Track C validator requires all ten).",
    )
    parser.add_argument(
        "--validation-only",
        action="store_true",
        help="Train/select on train+validation and save validation predictions without evaluating test.",
    )
    parser.add_argument(
        "--no-gradient-checkpointing",
        action="store_true",
        help="Disable encoder gradient checkpointing (uses more GPU memory).",
    )
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_rows(csv_path: Path) -> dict[str, list[dict[str, Any]]]:
    """Load canonical ``label`` or legacy ``label(intent)`` CSVs unchanged."""
    return load_track_c_rows(csv_path)


def whitespace_words(text: str) -> tuple[list[str], list[tuple[int, int]]]:
    """Return whitespace-delimited words and their character spans."""
    matches = list(re.finditer(r"\S+", text))
    return [match.group(0) for match in matches], [(m.start(), m.end()) for m in matches]


def resolve_slot_span(
    text: str,
    slot: dict[str, Any],
    occupied_char_spans: set[tuple[int, int]],
    csv_row: int,
) -> tuple[int, int]:
    """Use slots_json offsets, falling back to an unclaimed exact value match."""
    value = str(slot.get("value", ""))
    if not value:
        raise ValueError(f"Empty slot value in CSV row {csv_row}: {slot!r}")

    try:
        start, end = int(slot["start"]), int(slot["end"])
        if 0 <= start < end <= len(text) and text[start:end] == value:
            return start, end
    except (KeyError, TypeError, ValueError):
        pass

    candidates = [
        (match.start(), match.end())
        for match in re.finditer(re.escape(value), text)
        if (match.start(), match.end()) not in occupied_char_spans
    ]
    if not candidates:
        raise ValueError(
            f"Could not locate slot value {value!r} from slots_json in CSV row {csv_row}."
        )
    try:
        hint = int(slot.get("start", 0))
    except (TypeError, ValueError):
        hint = 0
    return min(candidates, key=lambda span: abs(span[0] - hint))


def make_word_slot_labels(
    row: dict[str, Any],
    slot_type_to_id: dict[str, int],
    slot_labels: list[str],
) -> tuple[list[str], list[str]]:
    """Project character spans onto whitespace words and create BIO labels."""
    text = row["text"]
    words, word_spans = whitespace_words(text)
    labels = ["O"] * len(words)
    occupied_words: set[int] = set()
    occupied_char_spans: set[tuple[int, int]] = set()

    for annotation in row["slots"]:
        slot_type = str(annotation["type"]).strip()
        if slot_type not in slot_type_to_id:
            raise ValueError(f"Unknown slot type {slot_type!r} in record {row['record_id']}.")
        char_span = resolve_slot_span(text, annotation, occupied_char_spans, row["csv_row"])
        occupied_char_spans.add(char_span)
        token_indices = [
            index
            for index, (word_start, word_end) in enumerate(word_spans)
            if word_start < char_span[1] and word_end > char_span[0]
        ]
        if not token_indices:
            raise ValueError(f"Slot span {char_span} maps to no words in record {row['record_id']}.")
        if any(index in occupied_words for index in token_indices):
            raise ValueError(
                f"Overlapping slot annotations map to the same word in record {row['record_id']}."
            )

        bio_type = slot_type
        labels[token_indices[0]] = f"B-{bio_type}"
        for index in token_indices[1:]:
            labels[index] = f"I-{bio_type}"
        occupied_words.update(token_indices)

    # Keep this parameter in the signature to make the vocabulary use explicit
    # and catch accidental BIO types that were omitted while constructing it.
    unknown = sorted(set(labels) - set(slot_labels))
    if unknown:
        raise ValueError(f"Generated slot labels are absent from label vocabulary: {unknown}")
    return words, labels


def augment_training_rows(rows: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    """Create conservative slot-value swaps using training rows only.

    Replacement values must have the same intent, slot type, and whitespace
    word count. Original examples are retained, slot character offsets are
    rebuilt, and validation/test rows are never consulted.
    """
    value_bank: dict[tuple[str, str, int], set[str]] = defaultdict(set)
    for row in rows:
        for slot in row["slots"]:
            value = str(slot.get("value", ""))
            value_bank[(row["intent"], str(slot["type"]), len(value.split()))].add(value)

    rng = random.Random(seed)
    known_texts = {(row["intent"], row["text"]) for row in rows}
    augmented: list[dict[str, Any]] = []
    for row in rows:
        replaceable: list[tuple[int, list[str]]] = []
        for index, slot in enumerate(row["slots"]):
            value = str(slot.get("value", ""))
            key = (row["intent"], str(slot["type"]), len(value.split()))
            candidates = sorted(candidate for candidate in value_bank[key] if candidate != value)
            if candidates:
                replaceable.append((index, candidates))
        if not replaceable:
            continue

        selected_index, candidates = rng.choice(replaceable)
        replacement = rng.choice(candidates)
        source_text = row["text"]
        ordered_slots = sorted(enumerate(row["slots"]), key=lambda item: int(item[1]["start"]))
        text_parts: list[str] = []
        new_slots: list[dict[str, Any]] = []
        cursor = 0
        output_length = 0
        replacement_details: Optional[tuple[str, str, str]] = None
        for original_index, slot in ordered_slots:
            start, end = int(slot["start"]), int(slot["end"])
            if start < cursor or source_text[start:end] != str(slot.get("value", "")):
                raise ValueError(
                    f"Cannot safely augment record {row['record_id']}: slot offsets do not match text."
                )
            unchanged_text = source_text[cursor:start]
            text_parts.append(unchanged_text)
            output_length += len(unchanged_text)

            value = replacement if original_index == selected_index else str(slot["value"])
            if original_index == selected_index:
                replacement_details = (str(slot["type"]), str(slot["value"]), replacement)
            new_start = output_length
            text_parts.append(value)
            output_length += len(value)
            new_slot = dict(slot)
            new_slot.update({"value": value, "start": new_start, "end": output_length})
            new_slots.append(new_slot)
            cursor = end

        text_parts.append(source_text[cursor:])
        augmented_text = "".join(text_parts)
        key = (row["intent"], augmented_text)
        if key in known_texts:
            continue
        known_texts.add(key)
        augmented_row = dict(row)
        augmented_row["record_id"] = f"{row['record_id']}#aug1"
        augmented_row["text"] = augmented_text
        augmented_row["slots"] = new_slots
        assert replacement_details is not None
        augmented_row["augmentation_source_record_id"] = row["record_id"]
        augmented_row["augmentation_slot_type"] = replacement_details[0]
        augmented_row["augmentation_original_value"] = replacement_details[1]
        augmented_row["augmentation_replacement_value"] = replacement_details[2]
        augmented.append(augmented_row)
    return augmented


def prepare_examples(
    rows: list[dict[str, Any]],
    tokenizer: Any,
    intent_to_id: dict[str, int],
    slot_type_to_id: dict[str, int],
    slot_label_to_id: dict[str, int],
    slot_labels: list[str],
    max_length: int,
) -> list[PreparedExample]:
    examples: list[PreparedExample] = []
    for row in rows:
        words, word_labels = make_word_slot_labels(row, slot_type_to_id, slot_labels)
        encoded = tokenizer(
            words,
            is_split_into_words=True,
            truncation=True,
            max_length=max_length,
            add_special_tokens=True,
            return_attention_mask=True,
        )
        if not hasattr(encoded, "word_ids"):
            raise RuntimeError(
                "A fast tokenizer with word_ids() support is required for sub-token alignment. "
                "Install a recent Transformers release and load the checkpoint tokenizer with use_fast=True."
            )
        word_ids = encoded.word_ids()
        aligned_slot_ids = [IGNORE_INDEX] * len(encoded["input_ids"])
        first_subtoken_mask = [0] * len(encoded["input_ids"])
        seen_word_ids: set[int] = set()
        for token_index, word_index in enumerate(word_ids):
            if word_index is None or word_index in seen_word_ids:
                continue
            seen_word_ids.add(word_index)
            first_subtoken_mask[token_index] = 1
            aligned_slot_ids[token_index] = slot_label_to_id[word_labels[word_index]]

        examples.append(
            PreparedExample(
                input_ids=list(encoded["input_ids"]),
                attention_mask=list(encoded["attention_mask"]),
                slot_labels=aligned_slot_ids,
                first_subtoken_mask=first_subtoken_mask,
                intent_label=intent_to_id[row["intent"]],
                text=row["text"],
                record_id=row["record_id"],
                words=words,
                word_labels=word_labels,
                slot_annotations=row["slots"],
            )
        )
    return examples


class JointCollator:
    """Dynamically pad batches, using -100 for slot-label padding."""

    def __init__(self, pad_token_id: int, pad_to_multiple_of: Optional[int] = None):
        self.pad_token_id = pad_token_id
        self.pad_to_multiple_of = pad_to_multiple_of

    def __call__(self, batch: list[PreparedExample]) -> dict[str, Any]:
        max_length = max(len(example.input_ids) for example in batch)
        if self.pad_to_multiple_of:
            unit = self.pad_to_multiple_of
            max_length = math.ceil(max_length / unit) * unit

        input_ids, attention_masks, slot_labels, first_subtoken_masks = [], [], [], []
        for example in batch:
            padding = max_length - len(example.input_ids)
            input_ids.append(example.input_ids + [self.pad_token_id] * padding)
            attention_masks.append(example.attention_mask + [0] * padding)
            slot_labels.append(example.slot_labels + [IGNORE_INDEX] * padding)
            first_subtoken_masks.append(example.first_subtoken_mask + [0] * padding)

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_masks, dtype=torch.long),
            "slot_labels": torch.tensor(slot_labels, dtype=torch.long),
            "first_subtoken_mask": torch.tensor(first_subtoken_masks, dtype=torch.bool),
            "intent_labels": torch.tensor([e.intent_label for e in batch], dtype=torch.long),
            "examples": batch,
        }


def resolve_precision(requested: str, device: torch.device) -> tuple[Optional[torch.dtype], bool]:
    """Return the autocast dtype and whether FP16 gradient scaling is required."""
    if device.type != "cuda" or requested == "no":
        return None, False
    if requested == "bf16":
        if not torch.cuda.is_bf16_supported():
            raise ValueError("BF16 was requested, but this CUDA device does not support it.")
        return torch.bfloat16, False
    if requested == "fp16":
        return torch.float16, True
    if torch.cuda.is_bf16_supported():
        return torch.bfloat16, False
    return torch.float16, True


def autocast_context(device: torch.device, dtype: Optional[torch.dtype]):
    if device.type == "cuda" and dtype is not None:
        return torch.autocast(device_type="cuda", dtype=dtype)
    return nullcontext()


def optimizer_parameter_groups(
    model: nn.Module,
    weight_decay: float,
    learning_rate: float,
) -> list[dict[str, Any]]:
    """Build AdamW groups with standard weight-decay exclusions."""
    no_decay_terms = ("bias", "LayerNorm.weight", "layer_norm.weight")
    decay, no_decay = [], []
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        (no_decay if any(term in name for term in no_decay_terms) else decay).append(parameter)
    return [
        {"params": decay, "lr": learning_rate, "weight_decay": weight_decay},
        {"params": no_decay, "lr": learning_rate, "weight_decay": 0.0},
    ]


@torch.no_grad()
def evaluate(
    model: JointTransformerModel,
    loader: DataLoader,
    device: torch.device,
    precision_dtype: Optional[torch.dtype],
    intent_labels: list[str],
    slot_labels: list[str],
    training_slot_values: set[tuple[str, str]],
    collect_errors: bool = False,
) -> dict[str, Any]:
    model.eval()
    total_loss = 0.0
    batch_count = 0
    gold_records: list[dict[str, Any]] = []
    predicted_frames: list[dict[str, Any]] = []

    for batch in loader:
        input_ids = batch["input_ids"].to(device, non_blocking=True)
        attention_mask = batch["attention_mask"].to(device, non_blocking=True)
        intent_targets = batch["intent_labels"].to(device, non_blocking=True)
        slot_targets = batch["slot_labels"].to(device, non_blocking=True)
        with autocast_context(device, precision_dtype):
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                intent_labels=intent_targets,
                slot_labels=slot_targets,
                first_subtoken_mask=batch["first_subtoken_mask"].to(device, non_blocking=True),
                decode_slots=True,
            )
        total_loss += float(outputs["loss"].detach().float().cpu())
        batch_count += 1

        predicted_intent_ids = outputs["intent_logits"].argmax(dim=-1).detach().cpu().tolist()
        crf_predictions = outputs["slot_predictions"]
        predicted_slot_ids = (
            None
            if crf_predictions is not None
            else outputs["slot_logits"].argmax(dim=-1).detach().cpu().tolist()
        )
        masks = batch["first_subtoken_mask"].tolist()
        for example_index, (example, pred_intent_id, mask_row) in enumerate(zip(
            batch["examples"],
            predicted_intent_ids,
            masks,
        )):
            predicted_tags: list[str] = []
            pred_slot_row = predicted_slot_ids[example_index] if predicted_slot_ids is not None else None
            if crf_predictions is not None:
                predicted_tags = [slot_labels[tag_id] for tag_id in crf_predictions[example_index]]
            elif pred_slot_row is not None:
                predicted_tags = [
                    slot_labels[pred_slot_row[token_index]]
                    for token_index, is_first in enumerate(mask_row)
                    if is_first
                ]

            gold_records.append(
                {
                    "record_id": example.record_id,
                    "text": example.text,
                    "intent": intent_labels[example.intent_label],
                    "slots": example.slot_annotations,
                }
            )
            predicted_frames.append(
                {
                    "intent": intent_labels[pred_intent_id],
                    "slots": bio_tags_to_char_slots(example.text, predicted_tags),
                }
            )

    scored = evaluate_track_c(
        gold_records,
        predicted_frames,
        train_slot_values=training_slot_values,
        labels=intent_labels,
    )
    scored["loss"] = total_loss / max(batch_count, 1)
    if not collect_errors:
        scored.pop("predictions", None)
        scored.pop("error_analysis", None)
        scored["unseen_slot_values"].pop("errors", None)
    return scored


def train_one_epoch(
    model: JointTransformerModel,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    scaler: torch.amp.GradScaler,
    device: torch.device,
    precision_dtype: Optional[torch.dtype],
    gradient_accumulation_steps: int,
    slot_loss_weight: float,
) -> tuple[float, int]:
    model.train()
    optimizer.zero_grad(set_to_none=True)
    total_loss = 0.0
    skipped_optimizer_steps = 0

    for batch_index, batch in enumerate(loader):
        input_ids = batch["input_ids"].to(device, non_blocking=True)
        attention_mask = batch["attention_mask"].to(device, non_blocking=True)
        intent_labels = batch["intent_labels"].to(device, non_blocking=True)
        slot_labels = batch["slot_labels"].to(device, non_blocking=True)

        group_start = (batch_index // gradient_accumulation_steps) * gradient_accumulation_steps
        group_size = min(gradient_accumulation_steps, len(loader) - group_start)
        with autocast_context(device, precision_dtype):
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                intent_labels=intent_labels,
                slot_labels=slot_labels,
                first_subtoken_mask=batch["first_subtoken_mask"].to(device, non_blocking=True),
                slot_loss_weight=slot_loss_weight,
            )
            loss = outputs["loss"]
        total_loss += float(loss.detach().float().cpu())
        scaled_loss = loss / group_size
        scaler.scale(scaled_loss).backward()

        is_accumulation_boundary = (batch_index + 1) % gradient_accumulation_steps == 0
        is_last_batch = batch_index + 1 == len(loader)
        if is_accumulation_boundary or is_last_batch:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scale_before_step = scaler.get_scale()
            scaler.step(optimizer)
            scaler.update()
            # FP16 GradScaler may skip an optimizer update on overflow. Advance
            # the LR schedule only when the optimizer actually took a step.
            if not scaler.is_enabled() or scaler.get_scale() >= scale_before_step:
                scheduler.step()
            else:
                skipped_optimizer_steps += 1
            optimizer.zero_grad(set_to_none=True)

    return total_loss / max(len(loader), 1), skipped_optimizer_steps


def save_json(path: Path, content: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def installed_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def save_run_manifest(
    args: argparse.Namespace,
    checkpoint_path: Path,
    split_rows: dict[str, list[dict[str, Any]]],
    intent_labels: list[str],
    device: torch.device,
    test_evaluated: bool,
) -> None:
    eval_path = Path(__file__).with_name("track_c_evaluation.py")
    baseline_path = Path(__file__).with_name("evaluate_track_c_baselines.py")
    manifest = {
        "track": "C",
        "model_name": args.model_name,
        "seed": args.seed,
        "dataset_path": str(args.data.resolve()),
        "dataset_sha256": sha256_file(args.data),
        "training_script": Path(__file__).name,
        "training_script_sha256": sha256_file(Path(__file__)),
        "evaluation_script": eval_path.name,
        "evaluation_script_sha256": sha256_file(eval_path),
        "baseline_script": baseline_path.name,
        "baseline_script_sha256": sha256_file(baseline_path) if baseline_path.is_file() else None,
        "checkpoint": checkpoint_path.name,
        "checkpoint_sha256": sha256_file(checkpoint_path),
        "split_sizes": {name: len(split_rows[name]) for name in VALID_SPLITS},
        "per_intent_split": {
            label: {
                split: sum(row["intent"] == label for row in split_rows[split])
                for split in VALID_SPLITS
            }
            for label in intent_labels
        },
        "test_evaluated": test_evaluated,
        "python_version": platform.python_version(),
        "device": str(device),
        "cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "package_versions": {
            name: installed_version(name)
            for name in ("torch", "transformers", "pandas", "numpy", "scikit-learn")
        },
        "run_arguments": {
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "learning_rate": args.learning_rate,
            "max_length": args.max_length,
            "precision": args.precision,
            "use_crf": args.use_crf,
            "augment_slot_values": args.augment_slot_values,
            "validation_only": args.validation_only,
        },
    }
    save_json(args.output_dir / "run_manifest.json", manifest)


def main() -> None:
    args = parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.gradient_accumulation_steps < 1:
        raise ValueError("epochs, batch-size and gradient-accumulation-steps must be positive.")
    if args.max_length < 8:
        raise ValueError("max-length must be at least 8 to accommodate special tokens and text.")

    set_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    precision_dtype, use_fp16_scaler = resolve_precision(args.precision, device)
    print(f"Device: {device}; mixed precision: {precision_dtype or 'off'}")

    split_rows = load_rows(args.data)
    validate_track_c_splits(split_rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Build model output vocabularies from training annotations only. This
    # avoids using validation/test labels to define the classifier schema.
    intent_labels = sorted({row["intent"] for row in split_rows["train"]})
    slot_types = sorted(
        {
            str(slot["type"]).strip()
            for row in split_rows["train"]
            for slot in row["slots"]
        }
    )
    training_slot_values = {
        (str(slot["type"]).strip(), normalize_slot_value(str(slot["value"])))
        for row in split_rows["train"]
        for slot in row["slots"]
    }
    unseen_intents = sorted(
        {
            row["intent"]
            for split in ("validation", "test")
            for row in split_rows[split]
            if row["intent"] not in intent_labels
        }
    )
    unseen_slot_types = sorted(
        {
            str(slot["type"]).strip()
            for split in ("validation", "test")
            for row in split_rows[split]
            for slot in row["slots"]
            if str(slot["type"]).strip() not in slot_types
        }
    )
    if unseen_intents or unseen_slot_types:
        raise ValueError(
            "Validation/test contains labels absent from training: "
            f"intents={unseen_intents}, slot_types={unseen_slot_types}."
        )
    if len(intent_labels) != args.expected_intents:
        raise ValueError(
            f"Expected {args.expected_intents} intent labels, found "
            f"{len(intent_labels)}: {intent_labels}."
        )
    print("Preset split sizes:", {name: len(split_rows[name]) for name in VALID_SPLITS})
    print(f"Intent labels ({len(intent_labels)}): {intent_labels}")
    print(f"Slot types ({len(slot_types)}): {slot_types}")

    augmented_training_rows: list[dict[str, Any]] = []
    if args.augment_slot_values:
        augmented_training_rows = augment_training_rows(split_rows["train"], seed=args.seed)
        print(
            "Conservative train-only slot-value augmentation:",
            f"{len(augmented_training_rows)} new examples from {len(split_rows['train'])} originals",
        )
        if augmented_training_rows:
            preview = [
                {
                    "source_record_ID": row["augmentation_source_record_id"],
                    "augmentation_record_ID": row["record_id"],
                    "intent": row["intent"],
                    "slot_type": row["augmentation_slot_type"],
                    "original_slot_value": row["augmentation_original_value"],
                    "replacement_slot_value": row["augmentation_replacement_value"],
                    "text": row["text"],
                    "slots_json": json.dumps(row["slots"], ensure_ascii=False),
                }
                for row in augmented_training_rows
            ]
            pd.DataFrame(preview).to_csv(
                args.output_dir / "slot_value_augmentation_preview.csv",
                index=False,
                encoding="utf-8-sig",
            )

    if not slot_types:
        raise ValueError("No slot types were found in slots_json; cannot build the slot head.")
    intent_to_id = {label: index for index, label in enumerate(intent_labels)}
    slot_type_to_id = {label: index for index, label in enumerate(slot_types)}
    slot_labels = ["O"]
    for slot_type in slot_types:
        slot_labels.extend((f"B-{slot_type}", f"I-{slot_type}"))
    slot_label_to_id = {label: index for index, label in enumerate(slot_labels)}

    # Tokenizer fast mode is needed for word_ids(), which supplies exact
    # first-sub-token positions even when a Kiswahili word is split into pieces.
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    if not tokenizer.is_fast:
        raise RuntimeError("The selected checkpoint did not provide a fast tokenizer.")
    tokenizer.model_max_length = args.max_length
    if tokenizer.pad_token_id is None:
        raise ValueError("The selected tokenizer has no pad token; define one before batching.")
    tokenizer.padding_side = "right"

    rows_for_preparation = dict(split_rows)
    rows_for_preparation["train"] = split_rows["train"] + augmented_training_rows
    prepared = {
        split: prepare_examples(
            rows=rows_for_preparation[split],
            tokenizer=tokenizer,
            intent_to_id=intent_to_id,
            slot_type_to_id=slot_type_to_id,
            slot_label_to_id=slot_label_to_id,
            slot_labels=slot_labels,
            max_length=args.max_length,
        )
        for split in VALID_SPLITS
    }

    pad_multiple = 8 if device.type == "cuda" else None
    collator = JointCollator(tokenizer.pad_token_id, pad_to_multiple_of=pad_multiple)
    loader_generator = torch.Generator()
    loader_generator.manual_seed(args.seed)
    # Only the training partition is shuffled; no rows move between the CSV's
    # preset train/validation/test boundaries.
    train_loader = DataLoader(
        JointDataset(prepared["train"]),
        batch_size=args.batch_size,
        shuffle=True,
        generator=loader_generator,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        collate_fn=collator,
    )
    validation_loader = DataLoader(
        JointDataset(prepared["validation"]),
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        collate_fn=collator,
    )
    test_loader = DataLoader(
        JointDataset(prepared["test"]),
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        collate_fn=collator,
    )

    model = JointTransformerModel(
        model_name=args.model_name,
        num_intents=len(intent_labels),
        num_slot_labels=len(slot_labels),
        slot_label_names=slot_labels,
        dropout=args.dropout,
        gradient_checkpointing=not args.no_gradient_checkpointing,
        use_crf=args.use_crf,
    ).to(device)
    parameter_groups = optimizer_parameter_groups(
        model=model,
        weight_decay=args.weight_decay,
        learning_rate=args.learning_rate,
    )
    optimizer = torch.optim.AdamW(parameter_groups, lr=args.learning_rate)
    lr_group_summary = sorted(
        {float(group["lr"]) for group in parameter_groups},
    )
    print(f"Optimizer learning rates: {lr_group_summary}")
    updates_per_epoch = math.ceil(len(train_loader) / args.gradient_accumulation_steps)
    total_training_steps = updates_per_epoch * args.epochs
    warmup_steps = int(total_training_steps * args.warmup_ratio)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_training_steps,
    )
    scaler = torch.amp.GradScaler("cuda", enabled=use_fp16_scaler)

    best_selection_key: tuple[float, float, float] | None = None
    best_epoch = 0
    epochs_without_improvement = 0
    checkpoint_path = args.output_dir / "best_model.pt"
    history: list[dict[str, Any]] = []

    for epoch in range(1, args.epochs + 1):
        train_loss, skipped_optimizer_steps = train_one_epoch(
            model=model,
            loader=train_loader,
            optimizer=optimizer,
            scheduler=scheduler,
            scaler=scaler,
            device=device,
            precision_dtype=precision_dtype,
            gradient_accumulation_steps=args.gradient_accumulation_steps,
            slot_loss_weight=args.slot_loss_weight,
        )
        validation_metrics = evaluate(
            model,
            validation_loader,
            device,
            precision_dtype,
            intent_labels,
            slot_labels,
            training_slot_values,
        )
        epoch_record = {
            "epoch": epoch,
            "train_loss": train_loss,
            "skipped_optimizer_steps": skipped_optimizer_steps,
            "validation": validation_metrics,
        }
        history.append(epoch_record)
        print(json.dumps(epoch_record, ensure_ascii=False))

        selection_key = (
            float(validation_metrics["full_frame_exact_match"]),
            float(validation_metrics["intent"]["macro_f1"]),
            float(validation_metrics["slot_exact_type_character_span_micro"]["f1"]),
        )
        if best_selection_key is None or selection_key > best_selection_key:
            best_selection_key = selection_key
            best_epoch = epoch
            epochs_without_improvement = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.early_stopping_patience:
                print(f"Early stopping after epoch {epoch}; best epoch was {best_epoch}.")
                break

    if not checkpoint_path.is_file():
        raise RuntimeError("Training ended without producing a best validation checkpoint.")
    model.load_state_dict(torch.load(checkpoint_path, map_location=device, weights_only=True))

    best_validation_metrics = evaluate(
        model,
        validation_loader,
        device,
        precision_dtype,
        intent_labels,
        slot_labels,
        training_slot_values,
        collect_errors=True,
    )
    validation_report = {
        key: value for key, value in best_validation_metrics.items() if key != "predictions"
    }
    validation_report["best_epoch"] = best_epoch
    validation_report["selection_key"] = list(best_selection_key or ())
    validation_report["examples"] = len(best_validation_metrics["predictions"])
    save_json(args.output_dir / "validation_metrics.json", validation_report)
    save_json(args.output_dir / "validation_predictions.json", best_validation_metrics["predictions"])

    if args.validation_only:
        save_run_manifest(args, checkpoint_path, split_rows, intent_labels, device, test_evaluated=False)
        print("Validation-only run complete. Test examples were not evaluated.")
        print(json.dumps(validation_report, ensure_ascii=False, indent=2))
        print(f"\nBest validation checkpoint: {checkpoint_path.resolve()}")
        return

    test_metrics = evaluate(
        model,
        test_loader,
        device,
        precision_dtype,
        intent_labels,
        slot_labels,
        training_slot_values,
        collect_errors=True,
    )
    test_report = {
        "intent": test_metrics["intent"],
        "slot_exact_type_character_span_micro": test_metrics["slot_exact_type_character_span_micro"],
        "full_frame_exact_match": test_metrics["full_frame_exact_match"],
        "full_frame_exact_count": test_metrics["full_frame_exact_count"],
        "json_validity": test_metrics["json_validity"],
        "unseen_slot_values": test_metrics["unseen_slot_values"],
        "loss": test_metrics["loss"],
        "examples": len(test_metrics["predictions"]),
    }
    result = {
        "model_name": args.model_name,
        "slot_decoder": "constrained_linear_chain_crf" if args.use_crf else "token_softmax",
        "slot_value_augmentation": {
            "enabled": args.augment_slot_values,
            "generated_examples": len(augmented_training_rows),
            "replacement_policy": "same intent, slot type, and whitespace word count",
        },
        "optimizer": {
            "learning_rate": args.learning_rate,
            "weight_decay": args.weight_decay,
            "learning_rate_groups": lr_group_summary,
        },
        "seed": args.seed,
        "best_epoch": best_epoch,
        "checkpoint_selection": {
            "split": "validation",
            "priority": [
                "full_frame_exact_match",
                "intent_macro_f1",
                "exact_type_character_span_slot_f1",
            ],
            "best_validation_key": list(best_selection_key or ()),
        },
        "best_validation": validation_report,
        "split_sizes": {name: len(split_rows[name]) for name in VALID_SPLITS},
        "per_intent_split": {
            label: {
                split: sum(row["intent"] == label for row in split_rows[split])
                for split in VALID_SPLITS
            }
            for label in intent_labels
        },
        "intent_labels": intent_labels,
        "slot_labels": slot_labels,
        "test": test_report,
        "error_analysis": test_metrics["error_analysis"],
        "training_history": history,
    }

    tokenizer_dir = args.output_dir / "tokenizer"
    tokenizer.save_pretrained(tokenizer_dir)
    save_json(args.output_dir / "label_mappings.json", {
        "intent_to_id": intent_to_id,
        "slot_label_to_id": slot_label_to_id,
        "slot_type_to_id": slot_type_to_id,
    })
    save_json(args.output_dir / "test_predictions.json", test_metrics["predictions"])
    save_json(args.output_dir / "metrics_and_errors.json", result)
    save_run_manifest(args, checkpoint_path, split_rows, intent_labels, device, test_evaluated=True)
    print("\nTest metrics and error analysis:")
    print(json.dumps({key: value for key, value in result.items() if key != "training_history"}, ensure_ascii=False, indent=2))
    print(f"\nBest checkpoint: {checkpoint_path.resolve()}")


if __name__ == "__main__":
    main()
