#!/usr/bin/env python3
"""Run the reference transient or prepare the interactive Xschem bench."""
import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
SIM = ROOT / "sim"
CARDS = {
    "typ": ("tntp49_5v", "typ"),
    "cold": ("wnwp49_5v", "best"),
    "hot": ("bnwp49_5v", "worst"),
}


def render(name, values):
    return re.sub(r"%%(\w+)%%", lambda match: str(values[match[1]]), (SIM / name).read_text())


def model_paths(models, corner):
    mos, res = CARDS[corner]
    paths = {
        "mos_card": models / "mos" / mos,
        "res_card": models / "res" / res / "ppr",
        "ota_model": ROOT / "models" / "vcr_low_total.spice",
        "bias_model": ROOT / "models" / "vcr_low_total_bias.spice",
        "clock_model": ROOT / "models" / "clock.spice",
    }
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    return paths


def prepare_xschem(models):
    schematic = ROOT / "schematic"
    netlist_dir = schematic / "netlist"
    netlist_dir.mkdir(exist_ok=True)
    support = render("xschem_support.spice.in", model_paths(models, "typ"))
    for folder in (schematic, netlist_dir):
        (folder / "bench_support.spice").write_text(support)
    shutil.copyfile(schematic / ".spiceinit", netlist_dir / ".spiceinit")


def make_bench(args, paths):
    start_delay = 100 if args.corner == "cold" else 0
    values = {
        "cp": f"{args.cp:g}", "cn": f"{args.cn:g}", "initial": "2.5",
        "adc_us": f"{88.1 + start_delay:g}", "dis_us": 88 + start_delay,
        "sample_us": 84 + start_delay,
    }
    if args.seeded:
        records = json.loads((SIM / "seeds.json").read_text())
        for row in records:
            if (row["corner"], row["cp"], row["cn"]) == (args.corner, args.cp, args.cn):
                values.update(initial=row["initial"], seed_voltage=row["seed_voltage"])
                break
        else:
            raise ValueError("No saved seed for this case. See sim/seeds.json for the measured points.")
    stop_us = (395 if args.seeded else 795) + start_delay
    mode = "seeded" if args.seeded else "startup"
    directory = ROOT / "runs" / f"{args.corner}_cp{args.cp:g}_cn{args.cn:g}_{mode}"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "bench.cir").write_text(render(f"{mode}.cir.in", values))
    (directory / "support.spice").write_text(render(f"support_{args.corner}.spice.in", {**paths, "stop_us": stop_us}))
    shutil.copyfile(ROOT / "schematic" / ".spiceinit", directory / ".spiceinit")
    return directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models-dir", type=Path, default=os.environ.get("SCL08_MODELS"),
                        help="SCL08 ngspice_models49 directory (or set SCL08_MODELS)")
    parser.add_argument("--corner", choices=CARDS, default="typ")
    parser.add_argument("--cp", type=float, default=11.79, help="P sensor capacitance in pF")
    parser.add_argument("--cn", type=float, default=10, help="N sensor capacitance in pF")
    parser.add_argument("--seeded", action="store_true", help="Use saved initial values from the matched sweep")
    parser.add_argument("--prepare-xschem", action="store_true", help="Generate nominal setup files for Xschem")
    args = parser.parse_args()
    if args.models_dir is None:
        parser.error("supply --models-dir or set SCL08_MODELS")
    if not all(math.isfinite(cap) and cap > 0 for cap in (args.cp, args.cn)):
        parser.error("both capacitances must be finite, positive numbers")
    if not args.prepare_xschem and args.corner != "typ" and not args.seeded:
        parser.error("use --seeded for the characterized cold and hot runs")
    models = args.models_dir.expanduser().resolve()

    try:
        if args.prepare_xschem:
            prepare_xschem(models)
            return
        directory = make_bench(args, model_paths(models, args.corner))
        result = subprocess.run(
            ["ngspice", "-b", "-r", "trace.raw", "-o", "run.log", "bench.cir"], cwd=directory
        )
        log = (directory / "run.log").read_text(errors="replace")
        if result.returncode or "No. of Data Rows" not in log or "simulation(s) aborted" in log.lower():
            raise ValueError(f"Simulation did not complete. See {directory / 'run.log'}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Waveforms: {directory / 'trace.raw'}")


if __name__ == "__main__":
    main()
