#!/usr/bin/env python3
"""Audit a Track C contribution CSV against the NLP Datathon handbook.

This checks structure and recorded evidence only. It cannot verify fluency,
permission, genuine independent review, or whether an intent is semantically
correct; those require the team and a competent Kiswahili reviewer.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
import argparse


EXPECTED_INTENTS = {
    "weather_query",
    "datetime_query",
    "alarm_set",
    "calendar_set",
    "calendar_query",
    "lists_createoradd",
    "lists_query",
    "play_music",
    "news_query",
    "qa_definition",
}
EXPECTED_SLOTS = {"location", "date", "time", "item", "term"}
ALLOWED_SOURCE_METHODS = {
    "original_human",
    "human_localised",
    "newly_annotated",
    "corrected_with_evidence",
}
ACCEPTED_REVIEW_STATUSES = {"self_reviewed", "independently_reviewed"}


def find_column(fieldnames: list[str], *names: str) -> str | None:
    normalized = {name.strip().lower(): name for name in fieldnames}
    for name in names:
        if name.strip().lower() in normalized:
            return normalized[name.strip().lower()]
    return None


def parse_slots(raw: str, row_number: int, text: str, issues: list[str]):
    try:
        slots = json.loads(raw or "[]")
    except json.JSONDecodeError as error:
        issues.append(f"CSV row {row_number}: invalid slots_json ({error.msg})")
        return []
    if not isinstance(slots, list):
        issues.append(f"CSV row {row_number}: slots_json must be a list")
        return []

    spans = []
    for slot in slots:
        if not isinstance(slot, dict):
            issues.append(f"CSV row {row_number}: slot entry must be an object")
            continue
        slot_type = slot.get("type")
        value = slot.get("value")
        try:
            start, end = int(slot["start"]), int(slot["end"])
        except (KeyError, TypeError, ValueError):
            issues.append(f"CSV row {row_number}: slot is missing integer start/end")
            continue
        if slot_type not in EXPECTED_SLOTS:
            issues.append(f"CSV row {row_number}: unsupported slot type {slot_type!r}")
        if not isinstance(value, str) or not (0 <= start < end <= len(text)):
            issues.append(f"CSV row {row_number}: invalid slot value or character range")
            continue
        if text[start:end] != value:
            issues.append(
                f"CSV row {row_number}: {slot_type!r} span {start}:{end} "
                f"does not equal its value {value!r}"
            )
        spans.append((start, end, slot_type, value))

    ordered = sorted(spans)
    for left, right in zip(ordered, ordered[1:]):
        if right[0] < left[1]:
            issues.append(
                f"CSV row {row_number}: overlapping slots "
                f"{left[2]} {left[0]}:{left[1]} and {right[2]} {right[0]}:{right[1]}"
            )
    return spans


def audit(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames or []
        rows = list(reader)

    columns = {
        "record_id": find_column(fields, "record_id", "record_ID"),
        "language": find_column(fields, "language"),
        "text": find_column(fields, "text"),
        "label": find_column(fields, "label", "label(intent)", "intent"),
        "slots_json": find_column(fields, "slots_json"),
        "source_dataset": find_column(fields, "source_dataset"),
        "source_version": find_column(fields, "source_version"),
        "source_record_id": find_column(fields, "source_record_id"),
        "source_url": find_column(fields, "source_url"),
        "source_method": find_column(fields, "source_method"),
        "permission": find_column(fields, "licence_or_permission", "license_or_permission"),
        "permission_evidence": find_column(fields, "permission_evidence_ref", "permission_evidence"),
        "contributor": find_column(fields, "contributor_code"),
        "reviewer": find_column(fields, "reviewer_code"),
        "review_status": find_column(fields, "review_status", "reviewer_status"),
        "group_id": find_column(fields, "group_id"),
        "split": find_column(fields, "split"),
    }
    permission_evidence_column = columns["permission_evidence"]
    issues: list[str] = []
    evidence_issues: list[str] = []
    missing = [name for name, column in columns.items() if column is None]
    for name in missing:
        issues.append(f"Missing required field: {name}")

    def value(row, key, default=""):
        column = columns.get(key)
        return (row.get(column, "") or "").strip() if column else default

    intents = Counter(value(row, "label") for row in rows)
    splits = Counter(value(row, "split") for row in rows)
    intent_splits = Counter((value(row, "label"), value(row, "split")) for row in rows)
    methods = Counter(value(row, "source_method") for row in rows)
    review_statuses = Counter(value(row, "review_status") for row in rows)
    permissions = Counter(value(row, "permission") or "<blank>" for row in rows)
    source_ids_not_applicable = 0
    private_permission_refs = Counter()
    contributor_reviewer_same = 0
    slot_records = Counter()
    slot_total = 0
    slot_type_counts = Counter()
    all_slot_values = set()
    slot_values_by_split = defaultdict(set)
    intent_slot_records = Counter()
    intent_slot_values = defaultdict(set)
    group_splits = defaultdict(set)
    record_ids = []
    texts = []

    for index, row in enumerate(rows, start=2):
        record_ids.append(value(row, "record_id"))
        texts.append(value(row, "text"))
        contributor, reviewer = value(row, "contributor"), value(row, "reviewer")
        if contributor and contributor == reviewer:
            contributor_reviewer_same += 1
        if value(row, "source_method") not in ALLOWED_SOURCE_METHODS:
            evidence_issues.append(
                f"CSV row {index}: source_method {value(row, 'source_method')!r} "
                "is not an allowed handbook value"
            )
        status = value(row, "review_status")
        if status not in ACCEPTED_REVIEW_STATUSES:
            evidence_issues.append(f"CSV row {index}: unaccepted review_status {status!r}")
        permission_ref = value(row, "permission_evidence")
        if not permission_ref:
            evidence_issues.append(f"CSV row {index}: missing permission_evidence_ref")
        elif permission_ref.startswith("private:"):
            private_id = permission_ref.removeprefix("private:").strip()
            if not private_id:
                evidence_issues.append(f"CSV row {index}: empty private permission record ID")
            else:
                private_permission_refs[private_id] += 1
        elif not (path.parent / permission_ref.split("#", 1)[0]).is_file():
            evidence_issues.append(
                f"CSV row {index}: permission_evidence_ref target does not exist: {permission_ref!r}"
            )
        if value(row, "split") == "test" and status != "independently_reviewed":
            evidence_issues.append(f"CSV row {index}: test record is not marked independently_reviewed")
        if value(row, "source_record_id").lower() in {"", "not_applicable", "n/a"}:
            source_ids_not_applicable += 1
        if value(row, "group_id"):
            group_splits[value(row, "group_id")].add(value(row, "split"))

        parsed = parse_slots(
            value(row, "slots_json"), index, value(row, "text"), issues
        )
        intent = value(row, "label")
        if parsed:
            intent_slot_records[intent] += 1
        slot_records[value(row, "split")] += bool(parsed)
        slot_total += len(parsed)
        for _, _, slot_type, slot_value in parsed:
            slot_values_by_split[value(row, "split")].add((slot_type, slot_value))
            all_slot_values.add((slot_type, slot_value))
            slot_type_counts[slot_type] += 1
            intent_slot_values[intent].add((slot_type, slot_value))

    expected_missing = sorted(EXPECTED_INTENTS - set(intents))
    unexpected = sorted(set(intents) - EXPECTED_INTENTS)
    unseen_test_values = sorted(
        slot_values_by_split.get("test", set()) - slot_values_by_split.get("train", set())
    )
    split_group_conflicts = sorted(
        group_id for group_id, group in group_splits.items() if len(group) > 1
    )
    slot_free_by_split = {
        split: max(count - slot_records[split], 0)
        for split, count in splits.items()
    }

    return {
        "file": str(path),
        "rows": len(rows),
        "columns": fields,
        "resolved_columns": columns,
        "missing_fields": missing,
        "intents": dict(sorted(intents.items())),
        "expected_intents_missing": expected_missing,
        "unexpected_intents": unexpected,
        "splits": dict(sorted(splits.items())),
        "per_intent_split": {
            label: {
                split: intent_splits[(label, split)]
                for split in ("train", "validation", "dev", "test")
                if intent_splits[(label, split)]
            }
            for label in sorted(intents)
        },
        "slot_bearing_records_by_split": dict(sorted(slot_records.items())),
        "slot_free_records_by_split": dict(sorted(slot_free_by_split.items())),
        "slot_annotations": slot_total,
        "slot_type_counts": dict(sorted(slot_type_counts.items())),
        "unique_slot_type_value_pairs": len(all_slot_values),
        "slot_coverage_by_intent": {
            label: {
                "rows": intents[label],
                "slot_bearing_rows": intent_slot_records[label],
                "unique_type_value_pairs": len(intent_slot_values[label]),
                "slot_types": sorted({slot_type for slot_type, _ in intent_slot_values[label]}),
            }
            for label in sorted(intents)
        },
        "slot_annotation_issues": issues,
        "recorded_evidence_issues": evidence_issues,
        "source_methods": dict(sorted(methods.items())),
        "review_statuses": dict(sorted(review_statuses.items())),
        "permission_values": dict(sorted(permissions.items())),
        "permission_evidence_field_present": permission_evidence_column is not None,
        "private_permission_evidence_references": dict(sorted(private_permission_refs.items())),
        "source_ids_not_applicable": source_ids_not_applicable,
        "contributors_equal_reviewers": contributor_reviewer_same,
        "cross_split_group_ids": split_group_conflicts,
        "unique_record_ids": len(set(record_ids)),
        "unique_texts": len(set(texts)),
        "unseen_test_slot_values": [
            {"type": slot_type, "value": slot_value}
            for slot_type, slot_value in unseen_test_values
        ],
        "unseen_test_slot_value_count": len(unseen_test_values),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=Path("Team_22_Dataset_Track_C.csv"))
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    result = audit(args.csv)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Track C structural audit: {result['file']}")
    print(f"Rows: {result['rows']} | unique IDs: {result['unique_record_ids']} | unique texts: {result['unique_texts']}")
    print("Intent counts:")
    for label, count in result["intents"].items():
        print(f"  {label}: {count}")
    print(f"Missing handbook intents: {', '.join(result['expected_intents_missing']) or 'none'}")
    print(f"Out-of-scope intents: {', '.join(result['unexpected_intents']) or 'none'}")
    print(f"Split counts: {result['splits']}")
    print(f"Slot-bearing records by split: {result['slot_bearing_records_by_split']}")
    print(f"Slot-free records by split: {result['slot_free_records_by_split']}")
    print(f"Slot annotations: {result['slot_annotations']} | span/schema issues: {len(result['slot_annotation_issues'])}")
    print(f"Slot annotations by type: {result['slot_type_counts']}")
    print(f"Unique exact slot type/value pairs: {result['unique_slot_type_value_pairs']}")
    print("Per-intent slot coverage (rows / slot-bearing / unique type-value pairs):")
    for label, counts in result["slot_coverage_by_intent"].items():
        print(
            f"  {label}: {counts['rows']} / {counts['slot_bearing_rows']} / "
            f"{counts['unique_type_value_pairs']} ({', '.join(counts['slot_types'])})"
        )
    print(f"Source methods: {result['source_methods']}")
    print(f"Permission values: {result['permission_values']}")
    print(f"Permission evidence field present: {result['permission_evidence_field_present']}")
    print(f"Private permission record references: {result['private_permission_evidence_references']}")
    print(f"Source record IDs marked not applicable or blank: {result['source_ids_not_applicable']}")
    print(f"Review status values: {result['review_statuses']}")
    print(f"Recorded evidence issues: {len(result['recorded_evidence_issues'])}")
    print(f"Group IDs crossing splits: {len(result['cross_split_group_ids'])}")
    print(f"Unseen test slot values: {result['unseen_test_slot_value_count']}")
    for issue in result["slot_annotation_issues"][:30]:
        print(f"  ISSUE: {issue}")
    if len(result["slot_annotation_issues"]) > 30:
        print(f"  ... {len(result['slot_annotation_issues']) - 30} more issues")
    for issue in result["recorded_evidence_issues"][:30]:
        print(f"  EVIDENCE: {issue}")
    if len(result["recorded_evidence_issues"]) > 30:
        print(f"  ... {len(result['recorded_evidence_issues']) - 30} more evidence issues")
    if result["recorded_evidence_issues"]:
        print("Resolve the recorded review-status evidence issues listed above.")
    else:
        print("All rows record an accepted review status and a permission reference. Private evidence is not included or independently verified by this audit.")


if __name__ == "__main__":
    main()
