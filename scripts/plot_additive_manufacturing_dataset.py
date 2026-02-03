#!/usr/bin/env python3
"""Generate a dataset summary plot for additive manufacturing surrogate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _stats(arr: np.ndarray):
    q1 = np.quantile(arr, 0.25, axis=0)
    med = np.quantile(arr, 0.5, axis=0)
    q3 = np.quantile(arr, 0.75, axis=0)
    return q1, med, q3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/additive_manufacturing_surrogate/data.npz"),
    )
    parser.add_argument(
        "--hyperparams",
        type=Path,
        default=Path("experiments/thermal_field_data/results/run_0/hyperparameters.json"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/thermal_field_data/figures/additive_manufacturing_dataset.png"),
    )
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    with np.load(args.data) as data:
        ts = data["ts"]
        temp = data["temp"]
        source = data["source"]
        combinations = data["combinations"]

    hp = json.loads(args.hyperparams.read_text())
    train_params = np.array(hp["data"]["training_parameters"], dtype=float)

    idxs = []
    for param in train_params:
        dists = np.linalg.norm(combinations - param[None, :], axis=1)
        idxs.append(int(np.argmin(dists)))
    train_idxs = np.array(sorted(set(idxs)))
    all_idxs = np.arange(combinations.shape[0])
    mask = np.ones_like(all_idxs, dtype=bool)
    mask[train_idxs] = False
    test_idxs = all_idxs[mask]

    temp_mean = temp.mean(axis=2)
    source_mean = source.mean(axis=2)

    train_temp_q1, train_temp_med, train_temp_q3 = _stats(temp_mean[train_idxs])
    test_temp_q1, test_temp_med, test_temp_q3 = _stats(temp_mean[test_idxs])
    train_src_q1, train_src_med, train_src_q3 = _stats(source_mean[train_idxs])
    test_src_q1, test_src_med, test_src_q3 = _stats(source_mean[test_idxs])

    fig, axes = plt.subplots(2, 1, figsize=(7, 5), dpi=200, sharex=True)

    ax = axes[0]
    ax.plot(ts, train_temp_med, label=f"Train median (n={len(train_idxs)})", color="#1f77b4")
    ax.fill_between(ts, train_temp_q1, train_temp_q3, color="#1f77b4", alpha=0.2)
    ax.plot(ts, test_temp_med, label=f"Test median (n={len(test_idxs)})", color="#ff7f0e")
    ax.fill_between(ts, test_temp_q1, test_temp_q3, color="#ff7f0e", alpha=0.2)
    ax.set_ylabel("Mean temperature (K)")
    ax.set_title("Additive Manufacturing Dataset Summary")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(ts, train_src_med, label="Train median", color="#1f77b4")
    ax.fill_between(ts, train_src_q1, train_src_q3, color="#1f77b4", alpha=0.2)
    ax.plot(ts, test_src_med, label="Test median", color="#ff7f0e")
    ax.fill_between(ts, test_src_q1, test_src_q3, color="#ff7f0e", alpha=0.2)
    ax.set_ylabel("Mean source (arb.)")
    ax.set_xlabel("Time (s)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(args.out)
    print(f"Saved {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
