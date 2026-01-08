#!/bin/bash
set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
VENV_PATH="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "Missing venv at $VENV_PATH" >&2
  exit 1
fi

# Activate venv and run the notebook headlessly.
source "$VENV_PATH/bin/activate"
cd "$PROJECT_DIR/experiments/spinning_rigid_body"
PYTHON="$VENV_PATH/bin/python"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=1

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute spinning_rigid_body.ipynb \
  --output spinning_rigid_body.executed.ipynb \
  --ExecutePreprocessor.timeout=0
