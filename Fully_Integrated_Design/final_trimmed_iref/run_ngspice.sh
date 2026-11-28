#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
model_dir="${SCL08_MODELS:-$HOME/pdk/scl08/ngspice_models49}"
mos="$model_dir/mos/tntp49_5v"
res="$model_dir/res/typ/ppr"
if [[ ! -f "$mos" || ! -f "$res" ]]; then
    printf '%s\n' "Set SCL08_MODELS to the installed SCL08 ngspice_models49 directory." >&2
    exit 1
fi
stop_us=2495
tag=readout
case "${1:-}" in
    "") ;;
    --smoke) stop_us=195; tag=smoke ;;
    *) printf '%s\n' "Usage: ./run_ngspice.sh [--smoke]" >&2; exit 2 ;;
esac
printf '.include "%s"\n.include "%s"\n' "$mos" "$res" > pdk.spice
sed "s/@STOP_US@/$stop_us/" support.spice.in > support.spice
ngspice -b -r "$tag.raw" -o "$tag.log" bench.cir
if ! grep -q '^No. of Data Rows : [1-9]' "$tag.log" || grep -qi 'simulation(s) aborted' "$tag.log"; then
    printf '%s\n' "Check $tag.log for an incomplete transient." >&2
    exit 1
fi
