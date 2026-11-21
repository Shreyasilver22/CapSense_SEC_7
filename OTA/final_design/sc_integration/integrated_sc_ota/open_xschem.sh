#!/usr/bin/env bash
set -euo pipefail

project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$project_dir"
exec xschem --rcfile "$project_dir/xschemrc" --command "xschem zoom_full" "$project_dir/sc_ota_integrated.sch"
