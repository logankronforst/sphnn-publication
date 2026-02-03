#!/usr/bin/env python3
"""Generate a dataset summary plot for thermal food processing."""
from __future__ import annotations

import argparse
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
        default=Path("data/thermal_food_processing_surrogate/data.npz"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/thermal_food_processing_surrogate/noiseless/figures/thermal_food_processing_dataset.png"),
    )
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    with np.load(args.data) as data:
        ts = data["ts_train"]
        ys_train = data["ys_train"][:2]
        us_train = data["us_train"][:2]
        ys_test = data["ys_vali"]
        us_test = data["us_vali"]

    train_a = ys_train[:, :, 0]
    train_b = ys_train[:, :, 1]

    test_a = ys_test[:, :, 0]
    test_b = ys_test[:, :, 1]

    qa1, meda, qa3 = _stats(test_a)
    qb1, medb, qb3 = _stats(test_b)

    train_u = us_train[:, :, 0]
    test_u = us_test[:, :, 0]
    qu1, medu, qu3 = _stats(test_u)

    fig, axes = plt.subplots(3, 1, figsize=(7, 6), dpi=200, sharex=True)

    ax = axes[0]
    ax.plot(ts, meda, color="#ff7f0e", label="Test median")
    ax.fill_between(ts, qa1, qa3, color="#ff7f0e", alpha=0.2, label="Test IQR")
    ax.plot(ts, train_a[0], color="#1f77b4", linewidth=1.2, label="Train 1")
    ax.plot(ts, train_a[1], color="#1f77b4", linestyle="--", linewidth=1.2, label="Train 2")
    ax.set_ylabel("T_A (K)")
    ax.set_title("Thermal Food Processing Dataset (n_D=2 train, n=15 test)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=7)

    ax = axes[1]
    ax.plot(ts, medb, color="#ff7f0e", label="Test median")
    ax.fill_between(ts, qb1, qb3, color="#ff7f0e", alpha=0.2, label="Test IQR")
    ax.plot(ts, train_b[0], color="#1f77b4", linewidth=1.2, label="Train 1")
    ax.plot(ts, train_b[1], color="#1f77b4", linestyle="--", linewidth=1.2, label="Train 2")
    ax.set_ylabel("T_B (K)")
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.plot(ts, medu, color="#ff7f0e", label="Test median")
    ax.fill_between(ts, qu1, qu3, color="#ff7f0e", alpha=0.2, label="Test IQR")
    ax.plot(ts, train_u[0], color="#1f77b4", linewidth=1.2, label="Train 1")
    ax.plot(ts, train_u[1], color="#1f77b4", linestyle="--", linewidth=1.2, label="Train 2")
    ax.set_ylabel("T_oven (K)")
    ax.set_xlabel("Time (s)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(args.out)
    print(f"Saved {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
