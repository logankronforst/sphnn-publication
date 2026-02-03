#!/usr/bin/env python3
"""Summarize additive manufacturing metrics for run_0 artifacts."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import numpy as np

MODELS = ["sPHNN", "sPHNN-LM", "cPHNN", "PHNN", "NODE"]
METRICS = [
    "end_to_end_train_rmse",
    "end_to_end_test_rmse",
    "latent_train_rmse",
    "latent_test_rmse",
]


def _collect_metrics(run_dir: Path) -> Dict[str, Dict[str, List[float]]]:
    summary: Dict[str, Dict[str, List[float]]] = {}
    for model in MODELS:
        summary[model] = {m: [] for m in METRICS}
        inst_dirs = sorted((run_dir / model).glob("instance_*/error_measures.npz"))
        for f in inst_dirs:
            data = np.load(f)
            for metric in METRICS:
                if metric in data:
                    summary[model][metric].append(float(np.array(data[metric]).squeeze()))
    return summary


def _format_iqr(values: List[float]) -> str:
    arr = np.asarray(values, dtype=float)
    q1, med, q3 = np.quantile(arr, [0.25, 0.5, 0.75])
    return f"{med:.3g} [{q1:.3g}, {q3:.3g}]"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=Path("experiments/thermal_field_data/results/run_0"),
        help="Run directory containing model artifacts.",
    )
    args = parser.parse_args()

    summary = _collect_metrics(args.run_dir)

    print(f"Run dir: {args.run_dir}\n")
    print("Model | End-to-end Train RMSE | End-to-end Test RMSE | n")
    print("--- | --- | --- | ---")
    for model in MODELS:
        train_vals = summary[model]["end_to_end_train_rmse"]
        test_vals = summary[model]["end_to_end_test_rmse"]
        if not train_vals or not test_vals:
            print(f"{model} | MISSING | MISSING | 0")
            continue
        print(f"{model} | {_format_iqr(train_vals)} | {_format_iqr(test_vals)} | {len(train_vals)}")

    print("\nLatent RMSE medians")
    for model in MODELS:
        test_vals = summary[model]["latent_test_rmse"]
        if not test_vals:
            print(f"{model}: MISSING")
            continue
        print(f"{model}: {_format_iqr(test_vals)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
