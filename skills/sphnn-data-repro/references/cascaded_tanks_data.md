# Cascaded Tanks Data and Artifacts

## Dataset Location
- Required file: `data/cascaded_tanks/dataBenchmark.mat`.
- Checksum (SHA256): `cb2f88d4388be4d3f2a24c6402fba804976aac5f2e1f26cda59ea0a38d016eab`.
- Source: 4TU dataset from Schoukens et al. (see `data/cascaded_tanks/README.md`).

## Notebook Entry Point
- Notebook: `experiments/cascaded_tanks/cascaded_tanks.ipynb`.
- Data load uses `scipy.io.loadmat` on `dataBenchmark.mat`.
- Path note (Linux): use POSIX-style joins; avoid Windows backslashes. The notebook should use:
  ```python
  data_dir = Path('../../data')
  file = data_dir / 'cascaded_tanks' / 'dataBenchmark.mat'
  ```

## Dataset Notes
- Training data: `yEst`, `uEst` (one trajectory), stacked into `(1, T, 1)`.
- Validation/test data: `yVal`, `uVal`.
- Time grid: `ts = 4.0 * arange(T)` (1024 steps, Ts = 4s).

## Visualization
- Use the notebook plot cell that overlays input/output for train and validation to generate a dataset figure.
- Save to `experiments/cascaded_tanks/figures/cascaded_tanks_dataset.png` (create the directory if needed).
- Keep the figure consistent across runs so comparisons stay aligned.

## Shared Storage
- Preferred shared layout mirrors the repo under `$STOCKYARD/logan-shared/sphnn-publication/`.
- Copy the dataset (keep local copy) with:
  - `mkdir -p $STOCKYARD/logan-shared/sphnn-publication/data/cascaded_tanks`
  - `rsync -av data/cascaded_tanks/dataBenchmark.mat $STOCKYARD/logan-shared/sphnn-publication/data/cascaded_tanks/`
- Keep `data/cascaded_tanks` in-repo after copying (no symlink).

## Saved Artifacts
- Model artifacts are cached under `experiments/cascaded_tanks/results/<run>/`:
  - `weights.eqx`
  - `history.npz`
  - `error_measures.npz`
- Use a new `save_dir` for reruns so baseline artifacts remain intact.
