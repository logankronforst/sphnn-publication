# Stable Port-Hamiltonian Neural Networks

This code base contains the code and model weights to reproduce the results from the paper: *Stable Port-Hamiltonian Neural Networks*.

## Installation

#### Using uv
```bash
uv sync
```

#### Using pip
```bash
pip install -r requirements.txt
```

## Notes on required data

The `cascaded tanks` and `additive manufacturing surrogate` experiments require data from external sources to be placed in the respective directories in `data/` as described in the corresponding notebooks and in [`data\additive_manufacturing_surrogate\README.md`](data\additive_manufacturing_surrogate\README.md)
The data pertaining to the remaining experiments is included within this codebase and has been provided with the explicit consent of the respective authors.

Trained model weights are included and are loaded per default in each script. To rerun any experiment change the `save_dir` variable in each notebook under the section "Set Hyperparameters" to the new directory where the weights from the rerun should be saved.

## Reproducing metrics and figures

Thermal food processing (Section 4.3):
- Summarize run_A0 metrics (n_A=3 by default):
  - `python scripts/report_thermal_food_processing_metrics.py`
- Regenerate dataset summary plot:
  - `python scripts/plot_thermal_food_processing_dataset.py`

Additive manufacturing surrogate (Section 4.4):
- Summarize run_0 metrics:
  - `python scripts/report_additive_manufacturing_metrics.py`
- Regenerate dataset summary plot:
  - `python scripts/plot_additive_manufacturing_dataset.py`

## Data caching

The spinning rigid body experiment caches generated trajectories to avoid regenerating on every run:

- Cache file: `data/spinning_rigid_body/rigid_body_dataset.npz`
- Regenerate: set `force_regen = True` in `experiments/spinning_rigid_body/spinning_rigid_body.ipynb` or delete the cache file

The same experiment also caches model artifacts per run under `experiments/spinning_rigid_body/results/run_0/`:

- Weights: `weights.eqx`
- History: `history.npz`
- Metrics: `error_measures.npz`
