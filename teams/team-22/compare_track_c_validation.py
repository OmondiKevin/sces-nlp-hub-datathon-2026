#!/usr/bin/env python3
"""Select among Track C model ablations using validation metrics only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_candidate(directory: Path) -> dict[str, Any]:
    manifest_path = directory / "run_manifest.json"
    metrics_path = directory / "validation_metrics.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    if manifest.get("test_evaluated") is not False:
        raise ValueError(f"{directory}: this candidate evaluated the test split.")
    if not manifest.get("dataset_sha256"):
        raise ValueError(f"{directory}: missing dataset hash in run manifest.")
    key = metrics.get("selection_key")
    expected = [
        float(metrics["full_frame_exact_match"]),
        float(metrics["intent"]["macro_f1"]),
        float(metrics["slot_exact_type_character_span_micro"]["f1"]),
    ]
    if key != expected:
        raise ValueError(f"{directory}: validation selection key does not match its metrics.")
    return {
        "name": directory.name,
        "directory": str(directory),
        "dataset_sha256": manifest["dataset_sha256"],
        "seed": manifest["seed"],
        "test_evaluated": manifest["test_evaluated"],
        "full_frame_exact_match": expected[0],
        "intent_macro_f1": expected[1],
        "exact_slot_f1": expected[2],
        "selection_key": expected,
        "model_settings": manifest["run_arguments"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, default=Path("validation_model_selection.md"))
    args = parser.parse_args()
    if len(args.candidate) < 2:
        parser.error("Provide at least two validation-only candidate directories.")
    candidates = [read_candidate(path) for path in args.candidate]
    data_hashes = {candidate["dataset_sha256"] for candidate in candidates}
    seeds = {candidate["seed"] for candidate in candidates}
    if len(data_hashes) != 1 or len(seeds) != 1:
        raise ValueError("Candidates must use the same dataset hash and random seed.")
    winner = max(candidates, key=lambda item: tuple(item["selection_key"]))

    lines = [
        "# Track C validation-only model selection",
        "",
        f"Dataset SHA-256: `{next(iter(data_hashes))}`  ",
        f"Seed: {next(iter(seeds))}  ",
        "Selection priority: full-frame exact match, then intent macro-F1, then exact-span slot F1.",
        "",
        "| Candidate | Full-frame exact match | Intent macro-F1 | Exact slot F1 | Test evaluated |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for candidate in candidates:
        settings = candidate["model_settings"]
        flags = " ".join(
            ["--use-crf" if settings["use_crf"] else "--no-crf"]
            + ["--augment-slot-values" if settings["augment_slot_values"] else "--no-slot-value-augmentation"]
        )
        lines.append(
            f"| {candidate['name']} | {candidate['full_frame_exact_match']:.4f} | "
            f"{candidate['intent_macro_f1']:.4f} | {candidate['exact_slot_f1']:.4f} | No |"
        )
        candidate["final_flags"] = flags
    lines.extend(
        [
            "",
            f"Selected validation candidate: **{winner['name']}**.",
            f"Final-run flags: `{winner['final_flags']}`.",
            "",
            "This selection used validation metrics only. Freeze this configuration, retrain it on the same train/validation split, then evaluate the test split once.",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Selected {winner['name']} from validation; report: {args.output.resolve()}")


if __name__ == "__main__":
    main()
