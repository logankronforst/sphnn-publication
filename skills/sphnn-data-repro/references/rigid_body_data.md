# Spinning Rigid Body Data and Cache

## Cache Location and Entry Point
- Cache file: `data/spinning_rigid_body/rigid_body_dataset.npz`.
- Notebook entry point: `experiments/spinning_rigid_body/spinning_rigid_body.ipynb` under `### Generate data (cached)`.
- Path handling: `project_dir = Path.cwd()` is adjusted when running from `experiments/` or `spinning_rigid_body/` so the cache resolves to repo-level `data/`.

## Generation Settings (Ground Truth)
- Parameters: `I = diag(1,2,3)`, `mu = 0.01` (set `mu = 0` for strictly conservative).
- Train grid: `t in [0, 50]` with `N = 1000` points.
- Test grid: `t in [0, 200]` with `N = 1000` points.
- Initial conditions: `x0s_train ~ Uniform(0,1)^3`, then squared component-wise (`x0s_train = x0s_train**2`), seed 0.
- Test ICs: `x0s_test = x0s_train**2` (deterministic from train ICs).
- Derivatives: analytic `dot(omega)` evaluated on each grid and flattened.

## Reproducibility Rules
- Use cached data by default; set `force_regen = True` only when changing generation settings.
- When regenerating, record the seed, time grids, `mu`, and cache filename in run notes.
- Keep the cache stable when comparing model variants so metrics reflect model changes, not dataset drift.
