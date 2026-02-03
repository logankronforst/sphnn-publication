#!/bin/bash
set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
VENV_PATH="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "Missing venv at $VENV_PATH" >&2
  exit 1
fi

DATA_DIR="$PROJECT_DIR/data/additive_manufacturing_surrogate"
if [ ! -f "$DATA_DIR/data.npz" ] || [ ! -f "$DATA_DIR/mesh.nas" ]; then
  echo "Missing dataset files in $DATA_DIR (need data.npz and mesh.nas)" >&2
  exit 1
fi

# Activate venv and run the notebook headlessly.
source "$VENV_PATH/bin/activate"
cd "$PROJECT_DIR/experiments/thermal_field_data"
PYTHON="$VENV_PATH/bin/python"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=1

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute additive_manufacturing_surrogate.ipynb \
  --output additive_manufacturing_surrogate.executed.ipynb \
  --ExecutePreprocessor.timeout=0
