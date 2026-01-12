# Reproducibility and Benchmarking Notes

## Core Principles
- Lock ground-truth data for comparisons: use cached rigid-body trajectories and a fixed cascaded tanks dataset file.
- Track every change that affects data or metrics (dataset source, cache regeneration, normalization changes).

## Rigid Body Checks
- Ensure the cache file is reused across reruns unless you intentionally change generation parameters.
- Validate energy behavior (conservative or dissipative) matches the chosen `mu`.
- Compare trajectory and derivative metrics on the same cached dataset.
- Cache checksum (SHA256): `9c2abdc17f9a33b1159342292613c327e3688b3e34801683afd48df15d41774e`.

## Cascaded Tanks Checks
- Verify the dataset file is unchanged (record checksum if needed).
- Confirm train/test normalization is derived from the same training data for all model variants.
- Compare `error_measures.npz` across models and runs for consistent RMSE reporting.
- Dataset checksum (SHA256): `cb2f88d4388be4d3f2a24c6402fba804976aac5f2e1f26cda59ea0a38d016eab`.

## Artifact Checklist
- `weights.eqx`: trained model weights
- `history.npz`: loss curves and training history
- `error_measures.npz`: stored metrics used for plots

## Reference Context
- Use `HACK.md` for experiment context, expected qualitative behaviors, and dataset summaries.
