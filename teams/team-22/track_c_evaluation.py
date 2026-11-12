"""Shared exact-span evaluation utilities for Track C models and baselines."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable


SLOT_TYPES = {"location", "date", "time", "item", "term"}
VALID_SPLITS = ("train", "validation", "test")
TRACK_C_INTENTS = {
    "alarm_set", "calendar_query", "calendar_set", "datetime_query",
    "lists_createoradd", "lists_query", "news_query", "play_music",
    "qa_definition", "weather_query",
}


def load_track_c_rows(csv_path: Path) -> dict[str, list[dict[str, Any]]]:
    """Read canonical/legacy Track C CSV headers into validated split rows."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset CSV not found: {csv_path.resolve()}")
    with csv_path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        columns = {str(name).strip().casefold(): name for name in (reader.fieldnames or [])}
        missing = [name for name in ("text", "slots_json", "split") if name not in columns]
        label_column = next(
            (columns[name] for name in ("label", "label(intent)", "intent") if name in columns),
            None,
        )
        if label_column is None:
            missing.append("label (or legacy label(intent))")
        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")
        rows = list(reader)

    split_rows: dict[str, list[dict[str, Any]]] = {split: [] for split in VALID_SPLITS}
    for row_index, row in enumerate(rows, start=2):
        text = row[columns["text"]]
        intent = row[label_column].strip()
        split = row[columns["split"]].strip().lower()
        if split not in VALID_SPLITS:
            raise ValueError(f"CSV row {row_index}: unsupported split {split!r}.")
        if not text.strip() or not intent:
            raise ValueError(f"CSV row {row_index}: text and intent must be non-empty.")
        try:
            slots = json.loads(row[columns["slots_json"]] or "[]")
        except json.JSONDecodeError as error:
            raise ValueError(f"CSV row {row_index}: invalid slots_json: {error}") from error
        if not isinstance(slots, list):
            raise ValueError(f"CSV row {row_index}: slots_json must be an array.")
        normalized_slots = []
        for slot in slots:
            if not isinstance(slot, dict) or not isinstance(slot.get("type"), str):
                raise ValueError(f"CSV row {row_index}: malformed slot record {slot!r}.")
            if slot["type"] not in SLOT_TYPES or not isinstance(slot.get("value"), str):
                raise ValueError(f"CSV row {row_index}: unsupported slot type/value {slot!r}.")
            try:
                start, end = int(slot["start"]), int(slot["end"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"CSV row {row_index}: slot needs integer start/end.") from error
            if not (0 <= start < end <= len(text)) or text[start:end] != slot["value"]:
                raise ValueError(f"CSV row {row_index}: slot offsets do not match the text.")
            normalized_slots.append(
                {"type": slot["type"], "value": slot["value"], "start": start, "end": end}
            )
        record_id_column = columns.get("record_id")
        group_id_column = columns.get("group_id")
        record_id = row.get(record_id_column, str(row_index - 2)) if record_id_column else str(row_index - 2)
        split_rows[split].append(
            {
                "record_id": record_id,
                "text": text,
                "intent": intent,
                "slots": normalized_slots,
                "group_id": row.get(group_id_column, "") if group_id_column else "",
                "csv_row": row_index,
            }
        )
    empty_splits = [split for split, split_rows_for_name in split_rows.items() if not split_rows_for_name]
    if empty_splits:
        raise ValueError(f"The CSV must include non-empty preset splits: {empty_splits}")
    return split_rows


def validate_track_c_splits(split_rows: dict[str, list[dict[str, Any]]]) -> None:
    """Enforce the finalized 250-row Track C label and 15/5/5 split contract."""
    all_rows = [row for rows in split_rows.values() for row in rows]
    if len(all_rows) != 250:
        raise ValueError(f"Track C requires exactly 250 rows; found {len(all_rows)}.")
    if len({str(row["record_id"]) for row in all_rows}) != len(all_rows):
        raise ValueError("Record IDs must be unique across all splits.")
    if len({str(row["text"]) for row in all_rows}) != len(all_rows):
        raise ValueError("Input texts must be unique across all splits.")
    group_splits: dict[str, set[str]] = {}
    for split, rows in split_rows.items():
        for row in rows:
            group_id = str(row.get("group_id", "")).strip()
            if group_id:
                group_splits.setdefault(group_id, set()).add(split)
    crossing_groups = sorted(group for group, splits in group_splits.items() if len(splits) > 1)
    if crossing_groups:
        raise ValueError(f"Group IDs cross data splits: {crossing_groups}.")
    observed_labels = {str(row["intent"]) for row in all_rows}
    if observed_labels != TRACK_C_INTENTS:
        raise ValueError(
            "Dataset labels do not match Track C. "
            f"Missing={sorted(TRACK_C_INTENTS - observed_labels)}; "
            f"unexpected={sorted(observed_labels - TRACK_C_INTENTS)}."
        )
    expected_per_split = {"train": 15, "validation": 5, "test": 5}
    for label in sorted(TRACK_C_INTENTS):
        label_rows = [row for row in all_rows if row["intent"] == label]
        if len(label_rows) != 25:
            raise ValueError(f"Track C requires exactly 25 records for {label}; found {len(label_rows)}.")
        for split, expected in expected_per_split.items():
            found = sum(row["intent"] == label for row in split_rows.get(split, []))
            if found != expected:
                raise ValueError(
                    f"Track C requires {expected} {split} records for {label}; found {found}."
                )


def normalize_slot_value(value: str) -> str:
    """Normalize whitespace and case for train/test surface-value membership."""
    return " ".join(str(value).split()).casefold()


def bio_tags_to_char_slots(text: str, tags: Iterable[str]) -> list[dict[str, Any]]:
    """Turn word-level BIO tags into the same character-span frame Sauti emits."""
    tag_list = list(tags)
    matches = list(re.finditer(r"\S+", text))
    words = [match.group(0) for match in matches]
    spans = [(match.start(), match.end()) for match in matches]
    entities: list[dict[str, Any]] = []
    active_type: str | None = None
    active_start: int | None = None

    def close_entity(end_word: int) -> None:
        nonlocal active_type, active_start
        if active_type is None or active_start is None or end_word <= active_start:
            active_type, active_start = None, None
            return
        start = spans[active_start][0]
        end = spans[end_word - 1][1]
        while start < end and unicodedata.category(text[start]).startswith("P"):
            start += 1
        while start < end and unicodedata.category(text[end - 1]).startswith("P"):
            end -= 1
        if start < end:
            entities.append(
                {
                    "type": active_type,
                    "value": text[start:end],
                    "start": start,
                    "end": end,
                }
            )
        active_type, active_start = None, None

    for index, raw_tag in enumerate(tag_list[: len(words)]):
        tag = str(raw_tag)
        if tag == "O":
            close_entity(index)
            continue
        prefix, separator, slot_type = tag.partition("-")
        if not separator or slot_type not in SLOT_TYPES:
            close_entity(index)
            continue
        if prefix == "B" or (prefix == "I" and active_type != slot_type):
            close_entity(index)
            active_type, active_start = slot_type, index
        elif prefix != "I":
            close_entity(index)
    close_entity(min(len(words), len(tag_list)))
    return entities


def _slot_key(slot: dict[str, Any]) -> tuple[str, int, int]:
    def offset(value: Any) -> int:
        if isinstance(value, bool):
            return -1
        try:
            return int(value)
        except (TypeError, ValueError, OverflowError):
            return -1

    slot_type = slot.get("type", "")
    return str(slot_type), offset(slot.get("start")), offset(slot.get("end"))


def _slot_metrics(gold_slots: list[dict[str, Any]], predicted_slots: list[dict[str, Any]]) -> dict[str, Any]:
    gold_counts = Counter(_slot_key(slot) for slot in gold_slots)
    predicted_counts = Counter(_slot_key(slot) for slot in predicted_slots)
    true_positive = sum((gold_counts & predicted_counts).values())
    false_positive = sum(predicted_counts.values()) - true_positive
    false_negative = sum(gold_counts.values()) - true_positive
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "gold_spans": sum(gold_counts.values()),
        "predicted_spans": sum(predicted_counts.values()),
    }


def _intent_metrics(
    records: list[dict[str, Any]], frames: list[dict[str, Any]], labels: list[str]
) -> dict[str, Any]:
    matrix = {gold: {predicted: 0 for predicted in labels} for gold in labels}
    per_label: dict[str, dict[str, float | int]] = {}
    correct = 0
    for record, frame in zip(records, frames):
        gold = str(record["intent"])
        predicted = str(frame.get("intent", ""))
        if gold in matrix and predicted in matrix[gold]:
            matrix[gold][predicted] += 1
        correct += int(predicted == gold)
    for label in labels:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in labels if other != label)
        fn = sum(matrix[label][other] for other in labels if other != label)
        support = sum(matrix[label].values())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label[label] = {
            "support": support,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }
    macro_f1 = sum(float(per_label[label]["f1"]) for label in labels) / max(len(labels), 1)
    return {
        "accuracy": correct / max(len(records), 1),
        "macro_f1": macro_f1,
        "per_label": per_label,
        "confusion_matrix": matrix,
        "examples": len(records),
    }


def _frame_is_valid_json(frame: Any, text: str, labels: set[str]) -> bool:
    try:
        decoded = json.loads(json.dumps(frame, ensure_ascii=False, allow_nan=False))
    except (TypeError, ValueError, OverflowError):
        return False
    if not isinstance(decoded, dict) or set(decoded) != {"intent", "slots"}:
        return False
    if (
        not isinstance(decoded["intent"], str)
        or decoded["intent"] not in labels
        or not isinstance(decoded["slots"], list)
    ):
        return False
    for slot in decoded["slots"]:
        if not isinstance(slot, dict) or set(slot) != {"type", "value", "start", "end"}:
            return False
        if (
            not isinstance(slot["type"], str)
            or slot["type"] not in SLOT_TYPES
            or not isinstance(slot["value"], str)
        ):
            return False
        start, end = slot["start"], slot["end"]
        if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
            return False
        if not (0 <= start < end <= len(text)) or text[start:end] != slot["value"]:
            return False
    return True


def evaluate_track_c(
    records: list[dict[str, Any]],
    predicted_frames: list[dict[str, Any]],
    train_slot_values: set[tuple[str, str]] | None = None,
    labels: list[str] | None = None,
) -> dict[str, Any]:
    """Score complete Track C frames against exact annotated character spans."""
    if len(records) != len(predicted_frames):
        raise ValueError("The number of records and predicted frames must match.")
    label_list = sorted(labels or {str(record["intent"]) for record in records})
    if not label_list:
        raise ValueError("At least one intent label is required for evaluation.")

    safe_frames: list[dict[str, Any]] = []
    gold_slots_by_record: list[list[dict[str, Any]]] = []
    predicted_slots_by_record: list[list[dict[str, Any]]] = []
    json_valid_count = 0
    exact_frame_count = 0
    predictions: list[dict[str, Any]] = []
    unseen_targets: list[dict[str, Any]] = []
    unseen_errors: list[dict[str, Any]] = []
    normalized_train_values = {
        (slot_type, normalize_slot_value(value))
        for slot_type, value in (train_slot_values or set())
    }
    unique_unseen_values: set[tuple[str, str]] = set()

    for record, raw_frame in zip(records, predicted_frames):
        text = str(record["text"])
        safe_frame = raw_frame if isinstance(raw_frame, dict) else {}
        intent = safe_frame.get("intent", "")
        raw_slots = safe_frame.get("slots", [])
        slots = raw_slots if isinstance(raw_slots, list) else []
        safe_frames.append(safe_frame)
        valid_json = _frame_is_valid_json(safe_frame, text, set(label_list))
        json_valid_count += int(valid_json)

        gold_slots = [
            {"type": str(slot["type"]), "value": str(slot["value"]), "start": int(slot["start"]), "end": int(slot["end"])}
            for slot in record.get("slots", [])
        ]
        predicted_slots = [
            slot if isinstance(slot, dict) else {"type": "__invalid_slot__", "start": -1, "end": -1}
            for slot in slots
        ]
        gold_slots_by_record.append(gold_slots)
        predicted_slots_by_record.append(predicted_slots)
        gold_keys = Counter(_slot_key(slot) for slot in gold_slots)
        predicted_keys = Counter(_slot_key(slot) for slot in predicted_slots)
        slots_exact = gold_keys == predicted_keys
        frame_exact = (
            valid_json
            and str(intent) == str(record["intent"])
            and slots_exact
        )
        exact_frame_count += int(frame_exact)

        unseen_for_record = []
        for slot in gold_slots:
            norm_value = normalize_slot_value(slot["value"])
            pair = (slot["type"], norm_value)
            if pair in normalized_train_values:
                continue
            unique_unseen_values.add(pair)
            correctly_found = _slot_key(slot) in predicted_keys
            unseen_entry = {
                "type": slot["type"],
                "value": slot["value"],
                "start": slot["start"],
                "end": slot["end"],
                "exact_match": correctly_found,
            }
            unseen_for_record.append(unseen_entry)
            unseen_targets.append({"record_id": record.get("record_id"), **unseen_entry})
            if not correctly_found:
                unseen_errors.append({"record_id": record.get("record_id"), "text": text, **unseen_entry})

        failed_tasks = []
        if str(intent) != str(record["intent"]):
            failed_tasks.append("intent")
        if not slots_exact:
            failed_tasks.append("slots")
        if not valid_json:
            failed_tasks.append("json_or_schema")
        predictions.append(
            {
                "record_id": record.get("record_id"),
                "text": text,
                "gold_frame": {"intent": record["intent"], "slots": gold_slots},
                "predicted_frame": safe_frame,
                "full_frame_exact_match": frame_exact,
                "json_valid": valid_json,
                "failed_tasks": failed_tasks,
                "unseen_gold_slots": unseen_for_record,
            }
        )

    intent_report = _intent_metrics(records, safe_frames, label_list)
    slot_report = _slot_metrics(
        [slot for row in gold_slots_by_record for slot in row],
        [slot for row in predicted_slots_by_record for slot in row],
    )
    unseen_correct = sum(bool(item["exact_match"]) for item in unseen_targets)
    return {
        "intent": intent_report,
        "slot_exact_type_character_span_micro": slot_report,
        "full_frame_exact_match": exact_frame_count / max(len(records), 1),
        "full_frame_exact_count": exact_frame_count,
        "json_validity": {
            "valid": json_valid_count,
            "total": len(records),
            "rate": json_valid_count / max(len(records), 1),
        },
        "unseen_slot_values": {
            "distinct_type_value_pairs": len(unique_unseen_values),
            "gold_unseen_slots": len(unseen_targets),
            "exactly_recovered": unseen_correct,
            "exact_recall": unseen_correct / len(unseen_targets) if unseen_targets else 0.0,
            "errors": unseen_errors,
        },
        "predictions": predictions,
        "error_analysis": [item for item in predictions if item["failed_tasks"]][:5],
    }
