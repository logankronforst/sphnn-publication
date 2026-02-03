#!/bin/bash
set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
VENV_PATH="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "Missing venv at $VENV_PATH" >&2
  exit 1
fi

DATA_FILE="$PROJECT_DIR/data/thermal_food_processing_surrogate/data.npz"
if [ ! -f "$DATA_FILE" ]; then
  echo "Missing dataset at $DATA_FILE" >&2
  exit 1
fi

# Activate venv and run the noisy experiment using the cached .npz dataset.
source "$VENV_PATH/bin/activate"
cd "$PROJECT_DIR/experiments/thermal_food_processing_surrogate/noisy"
PYTHON="$VENV_PATH/bin/python"

export THERMAL_FOOD_DATA_NPZ="$DATA_FILE"
export THERMAL_FOOD_NUM_TRAIN=2
export THERMAL_FOOD_NOISY_SAVE_DIR="$PROJECT_DIR/experiments/thermal_food_processing_surrogate/noisy/results/run_0"
export THERMAL_FOOD_NOISY_PARALLEL=0

export MPLBACKEND=Agg
export OMP_NUM_THREADS=1

"$PYTHON" main.py
