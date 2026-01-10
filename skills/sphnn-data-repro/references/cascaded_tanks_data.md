# Cascaded Tanks Data and Artifacts

## Dataset Location
- Required file: `data/cascaded_tanks/dataBenchmark.mat`.
- Source: 4TU dataset from Schoukens et al. (see `data/cascaded_tanks/README.md`).

## Notebook Entry Point
- Notebook: `experiments/cascaded_tanks/cascaded_tanks.ipynb`.
- Data load uses `scipy.io.loadmat` on `dataBenchmark.mat`.
- Note: the notebook currently uses Windows-style paths (`data_dir = Path(R'..\\..\\data')`). On Linux, prefer:
  ```python
  data_dir = Path('../../data')
  file = data_dir / 'cascaded_tanks' / 'dataBenchmark.mat'
  ```

## Dataset Notes
- Training data: `yEst`, `uEst` (one trajectory), stacked into `(1, T, 1)`.
- Validation/test data: `yVal`, `uVal`.
- Time grid: `ts = 4.0 * arange(T)` (1024 steps, Ts = 4s).

## Saved Artifacts
- Model artifacts are cached under `experiments/cascaded_tanks/results/<run>/`:
  - `weights.eqx`
  - `history.npz`
  - `error_measures.npz`
- Use a new `save_dir` for reruns so baseline artifacts remain intact.
