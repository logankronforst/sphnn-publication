#!/bin/bash
#SBATCH -J spinning-rigid-body
#SBATCH -p vm-small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00
#SBATCH -A ASC24027
#SBATCH -o slurm-%x-%j.out
#SBATCH -e slurm-%x-%j.err

set -euo pipefail

# Use Miniforge Python via the project-local venv.

# Activate project-local venv.
source /work/11039/logankronforst/ls6/projects/sphnn-publication/.venv/bin/activate
PYTHON=/work/11039/logankronforst/ls6/projects/sphnn-publication/.venv/bin/python

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
cd "$PROJECT_DIR/experiments/spinning_rigid_body"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute spinning_rigid_body.ipynb \
  --output spinning_rigid_body.executed.ipynb \
  --ExecutePreprocessor.timeout=0
