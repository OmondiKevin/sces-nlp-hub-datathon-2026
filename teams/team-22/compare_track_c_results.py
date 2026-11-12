#!/usr/bin/env python3
"""Compare the final Track C model with saved baselines on the same test set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


METRIC_KEYS = (
    "intent_accuracy",
    "intent_macro_f1",
    "slot_precision",
    "slot_recall",
    "slot_f1",
    "full_frame_exact_match",
    "json_validity",
    "unseen_slot_value_recall",
)


def summarize(metrics: dict[str, Any]) -> dict[str, float]:
    intent = metrics["intent"]
    slots = metrics["slot_exact_type_character_span_micro"]
    unseen = metrics["unseen_slot_values"]
    return {
        "intent_accuracy": float(intent["accuracy"]),
        "intent_macro_f1": float(intent["macro_f1"]),
        "slot_precision": float(slots["precision"]),
        "slot_recall": float(slots["recall"]),
        "slot_f1": float(slots["f1"]),
        "full_frame_exact_match": float(metrics["full_frame_exact_match"]),
        "json_validity": float(metrics["json_validity"]["rate"]),
        "unseen_slot_value_recall": float(unseen["exact_recall"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--baseline-metrics", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("track_c_comparison.md"))
    args = parser.parse_args()

    model_metrics_path = args.model_dir / "metrics_and_errors.json"
    manifest_path = args.model_dir / "run_manifest.json"
    model_metrics = json.loads(model_metrics_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    baselines = json.loads(args.baseline_metrics.read_text(encoding="utf-8"))
    model_labels = set(model_metrics.get("intent_labels", []))
    baseline_labels = set(baselines.get("test_labels", []))
    if model_labels != baseline_labels:
        raise ValueError("Model and baseline intent schemas differ.")
    if manifest.get("dataset_sha256") != baselines.get("dataset_sha256"):
        raise ValueError("Model and baseline artifacts do not match the same dataset/split file hash.")
    model_required = {
        "intent", "slot_exact_type_character_span_micro", "full_frame_exact_match",
        "json_validity", "unseen_slot_values",
    }
    if not model_required.issubset(model_metrics.get("test", {})):
        raise ValueError("The model metrics are missing required Track C test results.")

    systems = {"AfriBERTa joint model": summarize(model_metrics["test"])}
    for name, entry in baselines["systems"].items():
        systems[name] = summarize(entry["metrics"])
    column_names = {
        "intent_accuracy": "Intent accuracy",
        "intent_macro_f1": "Intent macro-F1",
        "slot_precision": "Exact slot precision",
        "slot_recall": "Exact slot recall",
        "slot_f1": "Exact slot F1",
        "full_frame_exact_match": "Full-frame exact match",
        "json_validity": "JSON/schema validity",
        "unseen_slot_value_recall": "Unseen-value exact recall",
    }
    lines = [
        "# Track C results on the frozen test set",
        "",
        f"Dataset SHA-256: `{manifest['dataset_sha256']}`  ",
        f"Test examples: {model_metrics['test']['examples']}  ",
        f"Model: `{model_metrics['model_name']}`; seed {model_metrics['seed']}; best epoch {model_metrics['best_epoch']}",
        "",
        "| System | " + " | ".join(column_names.values()) + " |",
        "| --- | " + " | ".join("---:" for _ in column_names) + " |",
    ]
    for name, scores in systems.items():
        values = " | ".join(f"{scores[key]:.4f}" for key in column_names)
        lines.append(f"| {name} | {values} |")
    lines.extend(
        [
            "",
            "All systems use the same frozen test set. Intent classifiers and the surface-value matcher were fit from training rows only. Slot F1 requires exact slot type and Unicode character start/end. Full-frame exact match also requires the complete slot set and valid frame schema.",
            "",
            "See the model and baseline metric JSON files for per-label F1, confusion matrices, per-record predictions, unseen-value errors, and up to five actual mistakes.",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote comparison report: {args.output.resolve()}")


if __name__ == "__main__":
    main()
