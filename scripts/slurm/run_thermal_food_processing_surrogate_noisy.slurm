#!/bin/bash
#SBATCH -J thermal-food-processing-noisy
#SBATCH -p gpu-a100-small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH -t 08:00:00
#SBATCH -A ASC24027
#SBATCH -o slurm-%x-%j.out
#SBATCH -e slurm-%x-%j.err

set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
DATA_FILE="$PROJECT_DIR/data/thermal_food_processing_surrogate/data.npz"

if [ ! -f "$DATA_FILE" ]; then
  echo "Missing dataset at $DATA_FILE" >&2
  exit 1
fi

# Use Miniforge Python via the project-local venv.
source "$PROJECT_DIR/.venv/bin/activate"
PYTHON="$PROJECT_DIR/.venv/bin/python"

cd "$PROJECT_DIR/experiments/thermal_food_processing_surrogate/noisy"

export THERMAL_FOOD_DATA_NPZ="$DATA_FILE"
export THERMAL_FOOD_NUM_TRAIN=2
export THERMAL_FOOD_NOISY_SAVE_DIR="$PROJECT_DIR/experiments/thermal_food_processing_surrogate/noisy/results/run_0"
export THERMAL_FOOD_NOISY_PARALLEL=0

export MPLBACKEND=Agg
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

"$PYTHON" main.py
