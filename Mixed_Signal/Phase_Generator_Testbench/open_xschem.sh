#!/bin/sh
cd "$(dirname "$0")"
exec xschem --rcfile "$PWD/xschemrc" "$PWD/schematic/phase_generator_tb.sch"
