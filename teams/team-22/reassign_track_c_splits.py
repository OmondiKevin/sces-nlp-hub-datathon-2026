#!/usr/bin/env python3
"""Create a fresh, balanced Track C holdout and update its source log together.

The existing 50-row test set was inspected during model development. This one-time
operation selects five records per intent from the former training split for the
new test split, moves the former test records into training, and keeps validation
unchanged. It changes no text, labels, annotations, or review evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError(f"No CSV header found in {path}.")
        return list(reader.fieldnames), list(reader)


def write_csv_atomic(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="", dir=path.parent, delete=False
    ) as temporary:
        writer = csv.DictWriter(temporary, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        temporary_path = Path(temporary.name)
    temporary_path.replace(path)


def column_map(fields: list[str]) -> dict[str, str]:
    return {field.strip().casefold(): field for field in fields}


def apply_reassignment(dataset_path: Path, source_log_path: Path, seed_label: str) -> dict[str, Any]:
    data_fields, data_rows = read_csv(dataset_path)
    log_fields, log_rows = read_csv(source_log_path)
    data_columns, log_columns = column_map(data_fields), column_map(log_fields)
    for required in ("record_id", "label", "split"):
        if required not in data_columns:
            raise ValueError(f"Dataset is missing {required!r}.")
    for required in ("record_id", "split"):
        if required not in log_columns:
            raise ValueError(f"Source log is missing {required!r}.")

    record_id_col = data_columns["record_id"]
    label_col = data_columns["label"]
    split_col = data_columns["split"]
    log_id_col, log_split_col = log_columns["record_id"], log_columns["split"]
    data_by_id = {row[record_id_col]: row for row in data_rows}
    log_by_id = {row[log_id_col]: row for row in log_rows}
    if len(data_by_id) != len(data_rows) or len(log_by_id) != len(log_rows):
        raise ValueError("Record IDs must be unique in both CSVs.")
    if set(data_by_id) != set(log_by_id):
        raise ValueError("Dataset and source log record IDs do not match exactly.")
    if len(data_rows) != 250:
        raise ValueError(f"Expected exactly 250 records; found {len(data_rows)}.")

    labels = sorted({row[label_col].strip() for row in data_rows})
    groups: dict[str, list[dict[str, str]]] = {label: [] for label in labels}
    for row in data_rows:
        groups[row[label_col].strip()].append(row)
    if len(labels) != 10 or any(len(group) != 25 for group in groups.values()):
        raise ValueError("Expected 10 intents with exactly 25 records each.")
    if any(log_by_id[row[record_id_col]][log_split_col] != row[split_col] for row in data_rows):
        raise ValueError("Dataset and source-log split assignments already differ.")
    if any(sum(row[split_col] == split for row in group) != target
           for group in groups.values()
           for split, target in (("train", 15), ("validation", 5), ("test", 5))):
        raise ValueError("Expected the original 15/5/5 split for every intent.")

    selected_test_ids: set[str] = set()
    for label, group in groups.items():
        former_train = [row for row in group if row[split_col] == "train"]
        if len(former_train) != 15:
            raise ValueError(f"Expected 15 former training records for {label}.")
        ranked = sorted(
            former_train,
            key=lambda row: (
                hashlib.sha256(f"{seed_label}|{row[record_id_col]}".encode("utf-8")).hexdigest(),
                row[record_id_col],
            ),
        )
        selected_test_ids.update(row[record_id_col] for row in ranked[:5])

    reassigned = []
    for row in data_rows:
        record_id = row[record_id_col]
        previous_split = row[split_col]
        if record_id in selected_test_ids:
            new_split = "test"
        elif previous_split == "test":
            new_split = "train"
        else:
            new_split = previous_split
        if new_split != previous_split:
            row[split_col] = new_split
            log_by_id[record_id][log_split_col] = new_split
            reassigned.append(
                {
                    "record_id": record_id,
                    "intent": row[label_col],
                    "previous_split": previous_split,
                    "new_split": new_split,
                }
            )

    write_csv_atomic(dataset_path, data_fields, data_rows)
    write_csv_atomic(source_log_path, log_fields, log_rows)
    return {
        "seed_label": seed_label,
        "rows": len(data_rows),
        "selection": "five per intent selected from former train by SHA-256 rank; former test moved to train",
        "reassigned_records": len(reassigned),
        "fresh_test_record_ids": sorted(selected_test_ids),
        "records": reassigned,
        "split_sizes": {
            split: sum(row[split_col] == split for row in data_rows)
            for split in ("train", "validation", "test")
        },
        "per_intent_split": {
            label: {
                split: sum(row[label_col] == label and row[split_col] == split for row in data_rows)
                for split in ("train", "validation", "test")
            }
            for label in labels
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("Team_22_Dataset_Track_C.csv"))
    parser.add_argument("--source-log", type=Path, default=Path("provenance/Team_22_Source_Log.csv"))
    parser.add_argument("--seed-label", default="team22-track-c-fresh-test-v1")
    parser.add_argument("--audit-out", type=Path, default=Path("provenance/track_c_split_reassignment.json"))
    parser.add_argument("--apply", action="store_true", help="Apply the reassignment to both CSVs.")
    args = parser.parse_args()
    if not args.apply:
        parser.error("Pass --apply to update the authoritative dataset and source log.")
    report = apply_reassignment(args.data, args.source_log, args.seed_label)
    args.audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.audit_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
