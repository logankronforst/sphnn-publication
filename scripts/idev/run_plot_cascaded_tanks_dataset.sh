#!/bin/bash
set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
VENV_PATH="$PROJECT_DIR/.venv"
DATA_FILE="$PROJECT_DIR/data/cascaded_tanks/dataBenchmark.mat"

if [ ! -d "$VENV_PATH" ]; then
  echo "Missing venv at $VENV_PATH" >&2
  exit 1
fi

if [ ! -f "$DATA_FILE" ]; then
  echo "Missing dataset at $DATA_FILE" >&2
  exit 1
fi

source "$VENV_PATH/bin/activate"
export MPLBACKEND=Agg

"$VENV_PATH/bin/python" "$PROJECT_DIR/scripts/plot_cascaded_tanks_dataset.py"
