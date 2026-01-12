#!/bin/bash
set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
VENV_PATH="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "Missing venv at $VENV_PATH" >&2
  exit 1
fi

DATA_FILE="$PROJECT_DIR/data/cascaded_tanks/dataBenchmark.mat"
if [ ! -f "$DATA_FILE" ]; then
  echo "Missing dataset at $DATA_FILE" >&2
  exit 1
fi

# Activate venv and run the notebook headlessly.
source "$VENV_PATH/bin/activate"
cd "$PROJECT_DIR/experiments/cascaded_tanks"
PYTHON="$VENV_PATH/bin/python"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=1

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute cascaded_tanks.ipynb \
  --output cascaded_tanks.executed.ipynb \
  --ExecutePreprocessor.timeout=0
