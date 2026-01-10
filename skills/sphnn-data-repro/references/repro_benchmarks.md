# Reproducibility and Benchmarking Notes

## Core Principles
- Lock ground-truth data for comparisons: use cached rigid-body trajectories and a fixed cascaded tanks dataset file.
- Track every change that affects data or metrics (dataset source, cache regeneration, normalization changes).

## Rigid Body Checks
- Ensure the cache file is reused across reruns unless you intentionally change generation parameters.
- Validate energy behavior (conservative or dissipative) matches the chosen `mu`.
- Compare trajectory and derivative metrics on the same cached dataset.

## Cascaded Tanks Checks
- Verify the dataset file is unchanged (record checksum if needed).
- Confirm train/test normalization is derived from the same training data for all model variants.
- Compare `error_measures.npz` across models and runs for consistent RMSE reporting.

## Artifact Checklist
- `weights.eqx`: trained model weights
- `history.npz`: loss curves and training history
- `error_measures.npz`: stored metrics used for plots

## Reference Context
- Use `HACK.md` for experiment context, expected qualitative behaviors, and dataset summaries.
