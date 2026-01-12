---
name: sphnn-data-repro
description: Data generation correctness, caching, and reproducibility guidance for the sPHNN repo. Use when running or re-running experiments, validating dataset paths, controlling cache regeneration, or benchmarking rigid body and cascaded tanks results.
---

# sPHNN Data Repro

## Overview
Use this skill to keep dataset generation, caching, and benchmarking consistent when reproducing experiments in this repo. Focus on locking ground-truth data, documenting when caches change, and keeping metrics comparable across runs.

## Workflow: Spinning Rigid Body Data Generation
- Load `references/rigid_body_data.md` for the exact cache path, time grids, and generation settings.
- Use the cached dataset by default; set `force_regen = True` only when generation parameters change.
- Record cache details (file path, seed, and time grids) in your run notes to keep comparisons valid.
- Cache checksum (SHA256): `9c2abdc17f9a33b1159342292613c327e3688b3e34801683afd48df15d41774e`.

## Workflow: Cascaded Tanks Data
- Load `references/cascaded_tanks_data.md` for the required external file and notebook path details.
- Notebook path should use `Path('../../data') / 'cascaded_tanks' / 'dataBenchmark.mat'` on Linux; avoid backslashes.
- Keep the dataset file stable; if you must update it, note the source and checksum in your run log.
- Use a new `save_dir` for reruns so baseline artifacts remain available for comparison.
- Copy `data/cascaded_tanks/dataBenchmark.mat` to `$STOCKYARD/logan-shared/sphnn-publication/data/cascaded_tanks/` with `rsync`, and keep the local copy for benchmarking.
- If the dataset is missing, download the 4TU zip and extract `dataBenchmark.mat` as documented in `data/cascaded_tanks/README.md`.
- Dataset checksum (SHA256): `cb2f88d4388be4d3f2a24c6402fba804976aac5f2e1f26cda59ea0a38d016eab`.

## Benchmarking Checklist
- Keep cached ground truth stable between model variants and reruns.
- Compare metrics from `error_measures.npz` and plots for long-horizon stability.
- Use `HACK.md` as the canonical benchmark context for expected behaviors.

## Status Reporting (PI Request)
Hi @Logan Kronforst, thanks for the update on the machine situation. Quick follow-up on SPHNN from yesterday.
Let me know the status (regarding SPHNN) of the below (done / in progress / blocked):
1. Clone/setup the repo (preferably on TACC if compute-heavy) and confirm it runs.
2. Download any required datasets and place them in a shared TACC folder the whole team can access (document the shared path).
3. Document the datasets + setup/run steps (paths, commands, configs) in our shared notes (send me the link or paste the key info).
4. Reproduce the core experiments from the paper and verify the reported metrics; save checkpoints/models/artifacts for later reuse.

## Compute Resource Guidance
- Prefer CPU (vm-small/CPU idev) for dataset prep, plots, and quick checks; use GPU only when training runtime justifies it.
- Request only the GPUs the code can use. These notebooks run on a single device unless you add explicit multi-GPU parallelism (e.g., JAX `pmap`/`pjit`).

## Run Scripts
- Use `scripts/idev/` for interactive runs and `scripts/slurm/` for batch runs.
- The agent should provide commands but let the user launch idev or sbatch jobs.

## Resources
- `references/rigid_body_data.md`
- `references/cascaded_tanks_data.md`
- `references/repro_benchmarks.md`
