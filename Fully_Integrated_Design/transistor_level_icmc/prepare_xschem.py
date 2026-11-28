#!/usr/bin/env python3
"""Generate local model includes for the integrated Xschem testbench."""
import argparse
import os
from pathlib import Path
import shutil
from types import SimpleNamespace

from run_icm import BASE, DEFAULT_CELL, ROOT, instantiate, model_paths, render, set_feedback_bank


def prepare(models_dir, tap, feedback_units):
    args = SimpleNamespace(
        name="xschem_prep", corner="typ", cp=11.79, cn=10.0, mode="mos",
        models_dir=models_dir, cycles=12, mi=9, bank=40, tap=tap, gear=True,
        cell=DEFAULT_CELL, feedback_units=feedback_units,
    )
    case, _, stop_us = instantiate(args)
    paths = model_paths(models_dir.resolve(), "typ")
    paths["clock_model"] = case / "clock_icm.spice"
    bench = set_feedback_bank(render("xschem_support.spice.in", paths), feedback_units)
    bench = bench.replace("chg chgb phase_trim08", "chg chgb cm_sample cm_sampleb phase_trim08")
    bench = bench.replace(
        "v(xicm.cm_x) v(xicm.cm_hold)",
        "v(cm_x) v(cm_hold) v(cm_sample) v(accum) i(vicmdd)",
    )
    bench = bench.replace("VOTA vdd ota_vdd 0", "VOTA vdd ota_vdd 0\nVICMDD vdd cmdd 0")
    bench = bench.replace(".tran 80n 795u", f".tran 80n {stop_us}u")
    draw = ROOT / "schematic"
    netlist_dir = draw / "netlist"
    netlist_dir.mkdir(exist_ok=True)
    for directory in (draw, netlist_dir):
        (directory / "bench_support.spice").write_text(bench)
    shutil.copyfile(BASE / "schematic" / ".spiceinit", netlist_dir / ".spiceinit")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models-dir", type=Path, default=os.getenv("SCL08_MODELS"))
    parser.add_argument("--tap", type=float, default=390)
    parser.add_argument("--feedback-units", type=int, default=60)
    args = parser.parse_args()
    if args.models_dir is None:
        parser.error("supply --models-dir or set SCL08_MODELS")
    if not 0 < args.tap < 667.0419 or args.feedback_units < 1:
        parser.error("supply a positive feedback bank and a sample tap between 0 and 667.0419 µm")
    prepare(args.models_dir, args.tap, args.feedback_units)


if __name__ == "__main__":
    main()
