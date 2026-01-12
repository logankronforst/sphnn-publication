#!/bin/bash
#SBATCH -J cascaded-tanks-a100
#SBATCH -p gpu-a100-small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH -t 04:00:00
#SBATCH -A ASC24027
#SBATCH -o slurm-%x-%j.out
#SBATCH -e slurm-%x-%j.err

set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
DATA_FILE="$PROJECT_DIR/data/cascaded_tanks/dataBenchmark.mat"

if [ ! -f "$DATA_FILE" ]; then
  echo "Missing dataset at $DATA_FILE" >&2
  exit 1
fi

# Use Miniforge Python via the project-local venv.
source "$PROJECT_DIR/.venv/bin/activate"
PYTHON="$PROJECT_DIR/.venv/bin/python"

cd "$PROJECT_DIR/experiments/cascaded_tanks"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute cascaded_tanks.ipynb \
  --output cascaded_tanks.executed.ipynb \
  --ExecutePreprocessor.timeout=0
