#!/bin/sh
cd "$(dirname "$0")"
exec xschem --rcfile "$PWD/xschemrc" "$PWD/schematic/capsense_integrated_tb.sch"
