#!/usr/bin/env bash
set -euo pipefail
schematic_dir=$(cd -- "$(dirname -- "$0")" && pwd)
python3 "$schematic_dir/../prepare_xschem.py" "$@"
cd -- "$schematic_dir"
exec xschem --rcfile "$schematic_dir/xschemrc" --command "xschem zoom_full" "$schematic_dir/sc_vcr_input_cm_scl08.sch"
