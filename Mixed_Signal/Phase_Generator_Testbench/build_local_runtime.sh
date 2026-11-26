#!/bin/sh
set -eu
cd "$(dirname "$0")"
project_root="$PWD"
# Requires autoconf, gperf, bison, flex, make and a C/C++ compiler.
# Obtain the pinned Icarus source first; see the top-level README.
cd runtime-src/iverilog
sh autoconf.sh
./configure --prefix="$project_root/runtime" --enable-libvvp --disable-readline
make -j4 CXXFLAGS='-O0 -g0 -fPIC' CFLAGS='-O0 -g0 -fPIC'
make install
