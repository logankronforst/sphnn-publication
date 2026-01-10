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

## Workflow: Cascaded Tanks Data
- Load `references/cascaded_tanks_data.md` for the required external file and notebook path details.
- Keep the dataset file stable; if you must update it, note the source and checksum in your run log.
- Use a new `save_dir` for reruns so baseline artifacts remain available for comparison.

## Benchmarking Checklist
- Keep cached ground truth stable between model variants and reruns.
- Compare metrics from `error_measures.npz` and plots for long-horizon stability.
- Use `HACK.md` as the canonical benchmark context for expected behaviors.

## Resources
- `references/rigid_body_data.md`
- `references/cascaded_tanks_data.md`
- `references/repro_benchmarks.md`
