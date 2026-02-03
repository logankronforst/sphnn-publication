#!/usr/bin/env python3
"""Summarize thermal food processing metrics for run_A0 artifacts."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import numpy as np

MODELS = ["sPHNN", "sPHNN-LM", "cPHNN", "PHNN", "NODE"]


def _load_metric(data: np.lib.npyio.NpzFile, primary: str, fallback: str | None = None) -> float | None:
    if primary in data:
        return float(np.array(data[primary]).squeeze())
    if fallback and fallback in data:
        return float(np.array(data[fallback]).squeeze())
    return None


def _collect_metrics(run_dir: Path) -> Dict[str, Dict[int, Dict[str, List[float]]]]:
    summary: Dict[str, Dict[int, Dict[str, List[float]]]] = {}
    for model in MODELS:
        summary[model] = {}
        if model == "sPHNN-LM":
            aug_dirs = sorted(run_dir.glob(f"{model}/augment_*/dat_2/noise_0.0"))
            for inst_root in aug_dirs:
                num_aug = int(inst_root.parent.name.split("_")[1])
                inst_dirs = sorted(inst_root.glob("instance_*/error_measures.npz"))
                vals = {"train_rmse": [], "test_rmse": []}
                for f in inst_dirs:
                    data = np.load(f)
                    train = _load_metric(data, "train_rmse", "rmse_train")
                    test = _load_metric(data, "test_rmse", "rmse_test")
                    if train is not None:
                        vals["train_rmse"].append(train)
                    if test is not None:
                        vals["test_rmse"].append(test)
                summary[model][num_aug] = vals
        else:
            aug_dirs = sorted(run_dir.glob(f"{model}/augment_*"))
            for aug_dir in aug_dirs:
                num_aug = int(aug_dir.name.split("_")[1])
                inst_dirs = sorted(aug_dir.glob("instance_*/error_measures.npz"))
                vals = {"train_rmse": [], "test_rmse": []}
                for f in inst_dirs:
                    data = np.load(f)
                    train = _load_metric(data, "train_rmse")
                    test = _load_metric(data, "test_rmse")
                    if train is not None:
                        vals["train_rmse"].append(train)
                    if test is not None:
                        vals["test_rmse"].append(test)
                summary[model][num_aug] = vals
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
        default=Path("experiments/thermal_food_processing_surrogate/noiseless/results/run_A0"),
        help="Run directory containing model artifacts.",
    )
    parser.add_argument(
        "--augment",
        type=int,
        default=3,
        help="Augmentation level to summarize (n_A).",
    )
    parser.add_argument(
        "--all-augmentations",
        action="store_true",
        help="Also print test RMSE medians for all augmentations.",
    )

    args = parser.parse_args()
    summary = _collect_metrics(args.run_dir)

    print(f"Run dir: {args.run_dir}")
    print(f"Augmentation n_A={args.augment}\n")
    print("Model | Train RMSE (median [Q1,Q3]) | Test RMSE (median [Q1,Q3]) | n")
    print("--- | --- | --- | ---")
    for model in MODELS:
        vals = summary.get(model, {}).get(args.augment, {})
        train = vals.get("train_rmse", [])
        test = vals.get("test_rmse", [])
        if not train or not test:
            print(f"{model} | MISSING | MISSING | 0")
            continue
        train_fmt = _format_iqr(train)
        test_fmt = _format_iqr(test)
        print(f"{model} | {train_fmt} | {test_fmt} | {len(train)}")

    if args.all_augmentations:
        print("\nTest RMSE medians by augmentation")
        for model in MODELS:
            entries = []
            for num_aug in sorted(summary.get(model, {})):
                test_vals = summary[model][num_aug].get("test_rmse", [])
                if not test_vals:
                    continue
                q1, med, q3 = np.quantile(np.asarray(test_vals, dtype=float), [0.25, 0.5, 0.75])
                entries.append(f"{num_aug}: {med:.3g} [{q1:.3g}, {q3:.3g}]")
            print(f"{model}: " + ", ".join(entries))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
