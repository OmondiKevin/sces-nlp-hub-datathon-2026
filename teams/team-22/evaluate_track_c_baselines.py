#!/usr/bin/env python3
"""Run train-only Track C intent and slot baselines on the preset test split."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Any

from track_c_evaluation import (
    evaluate_track_c,
    normalize_slot_value,
    validate_track_c_splits,
)


def read_dataset(path: Path) -> dict[str, list[dict[str, Any]]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames or []
        by_lower = {field.strip().lower(): field for field in fields}
        label_column = next(
            (by_lower[name] for name in ("label", "label(intent)", "intent") if name in by_lower),
            None,
        )
        required = {"text", "slots_json", "split"}
        missing = sorted(required - set(by_lower))
        if label_column is None:
            missing.append("label (or legacy label(intent))")
        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")
        rows = list(reader)

    splits: dict[str, list[dict[str, Any]]] = {"train": [], "validation": [], "test": []}
    for index, row in enumerate(rows, start=2):
        split = row[by_lower["split"]].strip().lower()
        if split not in splits:
            raise ValueError(f"CSV row {index}: unsupported split {split!r}.")
        text = row[by_lower["text"]]
        intent = row[label_column].strip()
        try:
            slots = json.loads(row[by_lower["slots_json"]] or "[]")
        except json.JSONDecodeError as error:
            raise ValueError(f"CSV row {index}: invalid slots_json: {error}") from error
        if not isinstance(slots, list):
            raise ValueError(f"CSV row {index}: slots_json must be an array.")
        normalized_slots = []
        for slot in slots:
            if not isinstance(slot, dict):
                raise ValueError(f"CSV row {index}: a slot is not an object.")
            start, end = int(slot["start"]), int(slot["end"])
            value = str(slot["value"])
            if text[start:end] != value:
                raise ValueError(f"CSV row {index}: slot offsets do not match the text.")
            normalized_slots.append(
                {"type": str(slot["type"]), "value": value, "start": start, "end": end}
            )
        record_id_column = by_lower.get("record_id")
        group_id_column = by_lower.get("group_id")
        record_id = row.get(record_id_column, str(index - 2)) if record_id_column else str(index - 2)
        splits[split].append(
            {
                "record_id": record_id,
                "group_id": row.get(group_id_column, "") if group_id_column else "",
                "text": text,
                "intent": intent,
                "slots": normalized_slots,
            }
        )
    if any(not rows for rows in splits.values()):
        raise ValueError("The dataset must have non-empty train, validation, and test splits.")
    validate_track_c_splits(splits)
    return splits


def surface_value_matcher(
    text: str,
    value_type_counts: dict[str, Counter[str]],
) -> list[dict[str, Any]]:
    """Match longest training slot values at token boundaries, with no test-derived lexicon."""
    candidates = []
    for normalized_value, type_counts in value_type_counts.items():
        if not normalized_value:
            continue
        slot_type = sorted(type_counts, key=lambda name: (-type_counts[name], name))[0]
        flexible_whitespace_value = r"\s+".join(
            re.escape(token) for token in normalized_value.split()
        )
        pattern = re.compile(
            (r"(?<!\w)" if normalized_value[0].isalnum() else "")
            + flexible_whitespace_value
            + (r"(?!\w)" if normalized_value[-1].isalnum() else ""),
            flags=re.IGNORECASE | re.UNICODE,
        )
        for match in pattern.finditer(text):
            start, end = match.span()
            candidates.append((start, -(end - start), -sum(type_counts.values()), end, slot_type))

    selected = []
    for start, negative_length, _, end, slot_type in sorted(candidates):
        if any(start < existing_end and end > existing_start for existing_start, existing_end, _ in selected):
            continue
        selected.append((start, end, slot_type))
    return [
        {"type": slot_type, "value": text[start:end], "start": start, "end": end}
        for start, end, slot_type in sorted(selected)
    ]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("Team_22_Dataset_Track_C.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/track_c_baselines"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
    except ImportError as error:
        raise SystemExit(
            "scikit-learn is required for the character TF-IDF baseline; "
            "install requirements-model.txt first."
        ) from error

    split_rows = read_dataset(args.data)
    train_rows = split_rows["train"]
    test_rows = split_rows["test"]
    train_labels = [row["intent"] for row in train_rows]
    test_labels = sorted(set(train_labels))
    counts = Counter(train_labels)
    majority_intent = sorted(counts, key=lambda label: (-counts[label], label))[0]

    classifier = make_pipeline(
        TfidfVectorizer(analyzer="char", ngram_range=(2, 5), sublinear_tf=True),
        LogisticRegression(max_iter=3000, random_state=args.seed),
    )
    classifier.fit([row["text"] for row in train_rows], train_labels)
    tfidf_intents = classifier.predict([row["text"] for row in test_rows]).tolist()
    majority_intents = [majority_intent] * len(test_rows)

    value_type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in train_rows:
        for slot in row["slots"]:
            value_type_counts[normalize_slot_value(slot["value"])][slot["type"]] += 1
    train_slot_values = {
        (slot["type"], normalize_slot_value(slot["value"]))
        for row in train_rows
        for slot in row["slots"]
    }

    outputs = {
        "intent_majority": [
            {"intent": intent, "slots": []} for intent in majority_intents
        ],
        "intent_char_tfidf_logistic_regression": [
            {"intent": intent, "slots": []} for intent in tfidf_intents
        ],
        "char_tfidf_empty_slot": [
            {"intent": intent, "slots": []} for intent in tfidf_intents
        ],
        "char_tfidf_plus_train_surface_value_matcher": [
            {
                "intent": intent,
                "slots": surface_value_matcher(row["text"], value_type_counts),
            }
            for row, intent in zip(test_rows, tfidf_intents)
        ],
    }
    definitions = {
        "intent_majority": "Most frequent train-split label; alphabetical tie break.",
        "intent_char_tfidf_logistic_regression": (
            "Character TF-IDF (2-5 grams) plus logistic regression; fit on train split only."
        ),
        "char_tfidf_empty_slot": (
            "Same train-only character TF-IDF intent predictions with no predicted slots."
        ),
        "char_tfidf_plus_train_surface_value_matcher": (
            "Same intent predictions plus longest non-overlapping exact surface values "
            "memorized from train slot annotations only."
        ),
    }
    metric_results = {}
    per_label_rows = []
    for name, frames in outputs.items():
        scored = evaluate_track_c(test_rows, frames, train_slot_values, labels=test_labels)
        metric_results[name] = {
            key: value for key, value in scored.items() if key not in {"predictions", "error_analysis"}
        }
        metric_results[name]["error_analysis"] = scored["error_analysis"]
        for label, values in scored["intent"]["per_label"].items():
            per_label_rows.append(
                {
                    "system": name,
                    "label": label,
                    **values,
                }
            )
        write_json(args.output_dir / f"{name}_predictions.json", scored["predictions"])

    report = {
        "track": "C",
        "dataset": str(args.data),
        "dataset_sha256": hashlib.sha256(args.data.read_bytes()).hexdigest(),
        "baseline_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "evaluation_script_sha256": hashlib.sha256(
            Path(__file__).with_name("track_c_evaluation.py").read_bytes()
        ).hexdigest(),
        "python_version": platform.python_version(),
        "scikit_learn_version": importlib.metadata.version("scikit-learn"),
        "split_sizes": {name: len(rows) for name, rows in split_rows.items()},
        "train_majority_label": majority_intent,
        "test_labels": test_labels,
        "seed": args.seed,
        "tfidf_logistic_regression": {
            "analyzer": "char",
            "ngram_range": [2, 5],
            "sublinear_tf": True,
            "logistic_regression_max_iter": 3000,
            "random_state": args.seed,
        },
        "protocol": "All fitted classifiers and remembered slot values use train split only.",
        "systems": {
            name: {"definition": definitions[name], "metrics": metric_results[name]}
            for name in outputs
        },
    }
    write_json(args.output_dir / "baseline_metrics.json", report)
    with (args.output_dir / "per_label_report.csv").open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=("system", "label", "support", "precision", "recall", "f1"))
        writer.writeheader()
        writer.writerows(per_label_rows)
    print(f"Saved Track C baseline results under {args.output_dir.resolve()}")
    for name, system in report["systems"].items():
        metrics = system["metrics"]
        slots = metrics["slot_exact_type_character_span_micro"]
        print(
            f"{name}: intent macro-F1={metrics['intent']['macro_f1']:.4f}; "
            f"exact slot P/R/F1={slots['precision']:.4f}/{slots['recall']:.4f}/{slots['f1']:.4f}; "
            f"frame EM={metrics['full_frame_exact_match']:.4f}; "
            f"JSON={metrics['json_validity']['rate']:.4f}"
        )


if __name__ == "__main__":
    main()
