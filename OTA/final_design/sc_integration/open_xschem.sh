#!/usr/bin/env bash
set -e
project_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
cd -- "$project_dir"
exec xschem --rcfile "$project_dir/xschemrc" "$project_dir/designs/sc_cmfb.sch"
