#!/bin/bash
#SBATCH -J additive-manufacturing
#SBATCH -p gpu-a100-small
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH -t 12:00:00
#SBATCH -A ASC24027
#SBATCH -o slurm-%x-%j.out
#SBATCH -e slurm-%x-%j.err

set -euo pipefail

PROJECT_DIR=/work/11039/logankronforst/ls6/projects/sphnn-publication
DATA_DIR="$PROJECT_DIR/data/additive_manufacturing_surrogate"

if [ ! -f "$DATA_DIR/data.npz" ] || [ ! -f "$DATA_DIR/mesh.nas" ]; then
  echo "Missing dataset files in $DATA_DIR (need data.npz and mesh.nas)" >&2
  exit 1
fi

# Use Miniforge Python via the project-local venv.
source "$PROJECT_DIR/.venv/bin/activate"
PYTHON="$PROJECT_DIR/.venv/bin/python"

EXEC_DIR="$PROJECT_DIR/experiments/thermal_field_data"
cd "$EXEC_DIR"

export MPLBACKEND=Agg
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export SPHNN_SKIP_PV=${SPHNN_SKIP_PV:-1}

NOTEBOOK="additive_manufacturing_surrogate.ipynb"
TMP_NB="$(mktemp "$EXEC_DIR/.tmp_additive_manufacturing_surrogate.XXXXXX.ipynb")"
export NOTEBOOK_SRC="$NOTEBOOK"
export NOTEBOOK_TMP="$TMP_NB"

cleanup() {
  rm -f "$TMP_NB"
}
trap cleanup EXIT

# Patch PyVista visualization cell for headless execution.
"$PYTHON" - <<'PY'
import json
import os
from pathlib import Path

src = Path(os.environ["NOTEBOOK_SRC"])
tmp = Path(os.environ["NOTEBOOK_TMP"])
skip_flag = os.environ.get("SPHNN_SKIP_PV", "1")

nb = json.loads(src.read_text())
for cell in nb.get("cells", []):
    if cell.get("cell_type") != "code":
        continue
    text = "".join(cell.get("source", []))
    if "pv.Plotter" in text or "BackgroundPlotter" in text:
        lines = text.splitlines()
        wrapped = [
            "import os",
            "if os.environ.get('SPHNN_SKIP_PV', '1') == '1':",
            "    print('Skipping PyVista visualization')",
            "else:",
        ]
        wrapped += ["    " + line for line in lines]
        cell["source"] = [line + "\n" for line in wrapped]

tmp.write_text(json.dumps(nb))
PY

"$PYTHON" -m nbconvert \
  --to notebook \
  --execute "$TMP_NB" \
  --ExecutePreprocessor.path="$EXEC_DIR" \
  --output additive_manufacturing_surrogate.executed.ipynb \
  --ExecutePreprocessor.timeout=0
