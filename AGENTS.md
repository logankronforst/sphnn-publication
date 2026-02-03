# Repository Guidelines

## Project Structure & Module Organization
- `dynax/`: core library code (models, training, evaluation, constraints).
- `experiments/`: notebooks and per-experiment results.
- `data/`: cached datasets and external data drops.
- `scripts/`: helper run scripts.

## Environment Setup (TACC + Python 3.11)
- Miniforge Python 3.11.14 at `/work/11039/logankronforst/ls6/miniforge3`.
- Create the venv: `/work/11039/logankronforst/ls6/miniforge3/bin/python -m venv .venv`.
- Activate and install: `source .venv/bin/activate` then `uv sync` (preferred) or `pip install -r requirements.txt`.
- JAX is pinned to Python 3.11 in this setup; avoid 3.10/3.12 for paper reproduction.

## Run and SLURM Commands
- Scripts live under `scripts/idev/` (interactive runs) and `scripts/slurm/` (batch runs).
- Local headless runs:
  - `bash scripts/idev/run_rigid_body.sh`
  - `bash scripts/idev/run_cascaded_tanks.sh`
  - `bash scripts/idev/run_thermal_food_processing_surrogate.sh`
  - `bash scripts/idev/run_additive_manufacturing_surrogate.sh`
- TACC jobs:
  - `sbatch scripts/slurm/run_spinning_rigid_body.slurm`
  - `sbatch scripts/slurm/run_cascaded_tanks.slurm`
  - `sbatch scripts/slurm/run_thermal_food_processing_surrogate.slurm`
  - `sbatch scripts/slurm/run_additive_manufacturing_surrogate.slurm`
  - logs: `slurm-*.out` / `slurm-*.err`
- Caution: idev/compute jobs should be run by the user; the agent should provide the exact commands to run but avoid launching jobs directly.
- Resource guidance: cascaded tanks prep/plots and quick tests are CPU-friendly; use vm-small/CPU idev when possible and request GPU only for longer training runs.
- Avoid wasting GPUs: request only the GPU count the code can use. These notebooks default to a single device; multi-GPU requires explicit parallelization (e.g., JAX `pmap`/`pjit` or distributed training), otherwise extra GPUs sit idle.

## Data, Caching, and Shared Storage
- Spinning rigid body cache: `data/spinning_rigid_body/rigid_body_dataset.npz` (set `force_regen = True` to regenerate).
- Spinning rigid body checksum (SHA256): `9c2abdc17f9a33b1159342292613c327e3688b3e34801683afd48df15d41774e`.
- Use cached datasets by default; only set `force_regen = True` when generation parameters change, and record cache details (path, seed, time grids) in run notes.
- Model artifacts live under `experiments/<experiment>/results/run_0/`.
- Store large generated data under `$STOCKYARD/logan-shared/` for group `G-826938` access and symlink into the repo, e.g. `ln -s $STOCKYARD/logan-shared/sphnn-publication data/shared`.
- Preferred shared layout mirrors the repo under `$STOCKYARD/logan-shared/sphnn-publication/`, e.g. cache at `$STOCKYARD/logan-shared/sphnn-publication/data/spinning_rigid_body/`.
- Cascaded tanks dataset: `data/cascaded_tanks/dataBenchmark.mat` (external).
- Cascaded tanks path (Linux): use `Path('../../data') / 'cascaded_tanks' / 'dataBenchmark.mat'` in notebooks; Windows-style backslashes break on POSIX.
- Cascaded tanks checksum (SHA256): `cb2f88d4388be4d3f2a24c6402fba804976aac5f2e1f26cda59ea0a38d016eab`.
- Cascaded tanks: keep the external dataset file stable; if updated, record source and checksum, and use a new `save_dir` for reruns to preserve baseline artifacts.
- Download cascaded tanks data (from repo root) if missing:
  - `curl -L -o /tmp/cascaded_tanks.zip https://data.4tu.nl/ndownloader/items/d4810b78-6cdd-48fe-8950-9bd601e5f47f/versions/1`
  - `unzip -p /tmp/cascaded_tanks.zip CascadedTanksFiles.zip > /tmp/CascadedTanksFiles.zip`
  - `unzip -p /tmp/CascadedTanksFiles.zip CascadedTanksFiles/dataBenchmark.mat > data/cascaded_tanks/dataBenchmark.mat`
- Copy cascaded tanks data (keep in both places) using `rsync`:
  - `mkdir -p $STOCKYARD/logan-shared/sphnn-publication/data/cascaded_tanks`
  - `rsync -av data/cascaded_tanks/dataBenchmark.mat $STOCKYARD/logan-shared/sphnn-publication/data/cascaded_tanks/`
- Keep `data/cascaded_tanks` in-repo after copying so benchmarks continue to read the local dataset (no symlink).
- Copy (keep data in both places) using `rsync`:
  - `mkdir -p $STOCKYARD/logan-shared/sphnn-publication/data/spinning_rigid_body`
  - `rsync -av data/spinning_rigid_body/rigid_body_dataset.npz $STOCKYARD/logan-shared/sphnn-publication/data/spinning_rigid_body/`
- Keep `data/spinning_rigid_body` in-repo after copying so benchmarks continue to read the local cache (no symlink).

## Paper Benchmarking Checklist (arXiv:2502.02480v2)
- Global settings: MSE loss + Adam; same steps/lr per model; Glorot uniform init; 2x16 hidden layers for Sections 4.1-4.3, 2x32 for additive manufacturing.
- Spinning rigid body (Section 4.1): compare energy E curves (interquartile mean/range). sPHNN/bPHNN/sPHNN-LM match energy; PHNN/NODE deviate; sPHNN-LM equilibrium distance ~0.010.
- Cascaded tanks (Section 4.2): 20 instances; RMSE on train/test; extended test adds 400s zero input after t=4096 and outputs should drain to 0. Appendix D checks overflow saturation.
- Thermal food processing (Section 4.3): n_D=2 trajectories of 280 samples; RMSE on 15 test trajectories across n_A/n_D; check stability beyond t=1395. Noise test uses n_A=3, n_D=2, evaluate on clean test.
- Additive manufacturing surrogate (Section 4.4): POD to 40-dim latent; RMSE over 25 trajectories should peak <30 then decay; NODE/PHNN diverge.
- Always cross-check `HACK.md` and update it with what matches, what breaks, and any training/testing changes; compare `error_measures.npz` and long-horizon stability plots between runs.

## Metrics Reproduction
- Thermal food processing summary table:
  - `python scripts/report_thermal_food_processing_metrics.py`
- Thermal food processing dataset plot:
  - `python scripts/plot_thermal_food_processing_dataset.py`
- Additive manufacturing summary table:
  - `python scripts/report_additive_manufacturing_metrics.py`
- Additive manufacturing dataset plot:
  - `python scripts/plot_additive_manufacturing_dataset.py`

## Status Reporting (PI Request)
Hi @Logan Kronforst, thanks for the update on the machine situation. Quick follow-up on SPHNN from yesterday.
Let me know the status (regarding SPHNN) of the below (done / in progress / blocked):
1. Clone/setup the repo (preferably on TACC if compute-heavy) and confirm it runs.
2. Download any required datasets and place them in a shared TACC folder the whole team can access (document the shared path).
3. Document the datasets + setup/run steps (paths, commands, configs) in our shared notes (send me the link or paste the key info).
4. Reproduce the core experiments from the paper and verify the reported metrics; save checkpoints/models/artifacts for later reuse.

## Coding Style & Naming Conventions
- Python: 4-space indentation, snake_case.
- Match existing structure; no formatter enforced.
- Notebook outputs use `.executed.ipynb` suffix.

## Testing Guidelines
- No automated test suite yet. If adding tests, use `pytest` under `tests/` with `test_*.py` naming.

## Commit & Pull Request Guidelines
- Short, imperative, sentence-case commits (example: "Add rigid body cache").
- PRs include a summary, reproduction steps, and note any data/artifacts or `HACK.md` updates.
