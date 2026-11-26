#!/bin/sh
set -eu
cd "$(dirname "$0")"
NGSPICE_HEADERS=${NGSPICE_HEADERS:-/usr/share/ngspice/scripts/src}
mkdir -p runtime/include/ngspice runtime/lib/ngspice
printf '#define NGSPICELIBDIR "%s/runtime/lib/ngspice"\n' "$PWD" > runtime/include/ngspice/config.h
gcc -shared -fPIC -O2 -I runtime/include -I "$NGSPICE_HEADERS" -I adapter -o runtime/lib/ngspice/ivlng.so adapter/icarus_shim.c
gcc -shared -fPIC -O2 -I "$NGSPICE_HEADERS" -I adapter -o runtime/lib/ngspice/ivlng.vpi adapter/vpi.c
