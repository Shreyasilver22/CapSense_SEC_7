#!/usr/bin/env python3
"""Simulate the SCL08 transistor-level input common-mode loop in the integrated readout."""
import argparse
import csv
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = Path(os.getenv("CAPSENSE_INTEGRATED_DIR", ROOT.parent)).expanduser().resolve()
ICMC = Path(os.getenv("CAPSENSE_ICMC_DIR", ROOT.parents[1] / "ICMC")).expanduser().resolve()
DEFAULT_CELL = ICMC / "models" / "icm_scl08.spice"
integrate_samples = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE))
from run_sc import model_paths, render


def set_feedback_bank(support, units):
    """Set the same PMOS feedback multiplicity on both SC branches."""
    pattern = r"(?m)^(MFB SUM OUT SUM SUM P W=20u L=10u M=)60(?= )"
    changed, count = re.subn(pattern, rf"\g<1>{units:d}",support)
    if count != 1:
        raise ValueError("Expected one 60-unit feedback subcircuit in the base bench")
    return changed


def instantiate(args):
    feedback_units = getattr(args, "feedback_units", 60)
    defaults = f"{args.corner}_cp{args.cp:g}_cn{args.cn:g}_{args.mode}"
    if feedback_units != 60:
        defaults += f"_fb{feedback_units}"
    case = args.name or defaults
    work = ROOT / "runs" / case
    work.mkdir(parents=True, exist_ok=True)
    paths = model_paths(args.models_dir.resolve(), args.corner)
    delay = 100 if args.corner == "cold" else 0
    stop_us = args.cycles * 100 - 5 + delay
    values = {"cp": f"{args.cp:g}", "cn": f"{args.cn:g}", "initial": "2.5",
              "adc_us": f"{88.1 + delay:g}", "dis_us": 88 + delay, "sample_us": 84 + delay}
    deck = render("startup.cir.in", values)
    support_file = "support_" + args.corner + ".spice.in"
    if args.mode == "mos":
        clock = paths["clock_model"].read_text()
        clk_model = work / "clock_icm.spice"
        main_ports = "rx rxb tx txb pre preb track trackb chg chgb params:"
        assert clock.count(main_ports) == 1
        clock = clock.replace(main_ports, main_ports.replace(" params:", " cm_sample cm_sampleb params:"))
        ladder_line = "XL80T v80 vlate RPP W=2.4u L=667.0419u"
        assert clock.count(ladder_line) == 1
        clock = clock.replace(ladder_line, f"XL80T1 v80 vcm_sample RPP W=2.4u L={args.tap:g}u\n"
                              f"XL80T2 vcm_sample vlate RPP W=2.4u L={667.0419-args.tap:g}u")
        clock = clock.replace("XTR1 trackb track vdd vss inv08 w=20u",
                              "XTR1 trackb track vdd vss inv08 w=20u\n"
                              "XICMQ vcm_sample sensed cm_late vdd vss nb compare08\n"
                              "XICMEN cm_late track cm_sampleb vdd vss nand08\n"
                              "XICMBUF cm_sampleb cm_sample vdd vss inv08 w=10u")
        clk_model.write_text(clock)
        paths["clock_model"] = clk_model
    support = render(support_file, {**paths, "stop_us": stop_us})
    support = set_feedback_bank(support, feedback_units)
    if args.corner == "cold":
        support = support.replace(" i(vexC)", "")
    if args.mode in ("mos","off"):
        if args.mode == "mos":
            replacement = 'VICMDD vdd cmdd 0\n' + (
                "XICM sump sumn vref phi1 phi1b phit phitb phi2 cmdd 0 cm_sample cm_sampleb cm_x cm_hold accum "
                f"icm_cell08 mi={args.mi:d} drive_w={args.bank:d}\n"
            )
            deck = deck.replace('.include "support.spice"',
                    f'.include "support.spice"\n.include "{args.cell.resolve()}"')
            support = support.replace("chg chgb phase_trim08", "chg chgb cm_sample cm_sampleb phase_trim08")
            support = support.replace(" v(cm_sample)", " v(cm_sample) v(accum) i(vicmdd) v(xicm.drive) v(xclk.vcm_sample)")
        else:
            replacement = ""
            support = support.replace(" v(cm_x) v(cm_hold) v(cm_sample)", "")
        deck, count = re.subn(r"(?ms)^MCORRp .*?^BICMDRIVE [^\n]+\n", replacement, deck)
        assert count == 1
    if args.gear:
        support = support.replace(".options klu method=trap ", ".options method=gear ")
        support = support.replace(".options klu method=gear ", ".options method=gear ")
    (work / "bench.cir").write_text(deck)
    (work / "support.spice").write_text(support)
    shutil.copyfile(BASE / "schematic" / ".spiceinit", work / ".spiceinit")
    return work, delay, stop_us


def read_raw(file):
    header, body = file.read_bytes().split(b"Binary:\n", 1)
    lines = header.decode("ascii").splitlines()
    names = [line.split()[1] for line in lines[lines.index("Variables:") + 1:]]
    raw = np.frombuffer(body, dtype="<f8").reshape(-1, len(names))
    return {name: raw[:, i] for i, name in enumerate(names)}


def measure(waves, delay, cycles, supply):
    time_us = waves["time"] * 1e6
    at = lambda key, moment: float(np.interp(moment, time_us, waves[key]))
    rows = []
    for cycle in range(cycles):
        t0 = delay + cycle * 100
        def dv(a, b, t):
            return at(a, t0 + t) - at(b, t0 + t)
        def cm(a, b, t):
            return (at(a, t0 + t) + at(b, t0 + t)) / 2
        past = (time_us > t0 - 5) & (time_us < t0 + 95)
        win = np.r_[max(t0-5, 0), time_us[past], t0+95]
        avg = lambda key: integrate_samples(np.interp(win, time_us, waves[key]), win)/(win[-1] - win[0])
        corrected = "v(cm_sample)" in waves
        row = dict(cycle=cycle + 1, input_cm_at_85_V=cm("v(sump)", "v(sumn)", 85),
                   output_cm_at_85_V=cm("v(outp)", "v(outn)", 85),
                   live_at_85_mV=dv("v(outp)", "v(outn)", 85) * 1e3,
                   held_at_88_mV=dv("v(pinp)", "v(pinn)", 88) * 1e3,
                   adc_at_89_mV=dv("v(adcp)", "v(adcn)", 89) * 1e3,
                   vdd_mW=-supply*avg("i(vdd)")*1e3)
        if corrected:
            row.update(correction_gate_V=at("v(cm_x)",t0+85), hold_V=at("v(cm_hold)",t0+85))
        if "i(vicmdd)" in waves:
            row.update(controller_uW=supply*avg("i(vicmdd)")*1e6, integrator_V=at("v(accum)",t0+88))
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models-dir", type=Path, default=os.getenv("SCL08_MODELS"))
    parser.add_argument("--mode", choices=("mos", "off", "ideal"), default="mos")
    parser.add_argument("--corner", choices=("typ", "cold", "hot"), default="typ")
    parser.add_argument("--cp", type=float, default=11.79)
    parser.add_argument("--cn", type=float, default=10)
    parser.add_argument("--cycles", type=int, default=12)
    parser.add_argument("--mi", type=int, default=9)
    parser.add_argument("--bank", type=int, default=40)
    parser.add_argument("--tap", type=float, default=390)
    parser.add_argument("--name")
    parser.add_argument("--gear", action="store_true")
    parser.add_argument("--feedback-units", type=int, default=60,
                        help="PMOS feedback capacitor units per branch (default 60)")
    parser.add_argument("--cell", type=Path, default=DEFAULT_CELL)
    args = parser.parse_args()
    if args.models_dir is None:
        parser.error("provide --models-dir or set SCL08_MODELS")
    if args.cycles < 1 or min(args.mi, args.bank, args.feedback_units) < 1:
        parser.error("cycles and MOS capacitor multiplicities must be positive")
    if not all(math.isfinite(c) and c > 0 for c in (args.cp, args.cn)):
        parser.error("both sensor capacitances must be finite and positive")
    if not 0 < args.tap < 667.0419:
        parser.error("the sample tap must be between 0 and 667.0419 um")
    work, delay, stop = instantiate(args)
    with (work / "console.log").open("w") as console:
        result = subprocess.run(["ngspice","-b","-r","trace.raw","-o","run.log","bench.cir"],
                                stdout=console, stderr=subprocess.STDOUT, cwd=work)
    if result.returncode != 0 or not (work / "trace.raw").is_file():
        sys.exit(f"ngspice failed. See {work / 'run.log'}")
    waves = read_raw(work / "trace.raw")
    actual = waves["time"][-1]*1e6
    if abs(actual-stop) > .01:
        sys.exit(f"Transient aborted at {actual:.3f} instead of {stop} us. See {work / 'run.log'}")
    rows = measure(waves, delay, args.cycles, {"typ":5,"cold":4.5,"hot":5.5}[args.corner])
    with (work / "samples.csv").open("w") as output:
        table = csv.DictWriter(output, fieldnames=rows[0].keys())
        table.writeheader()
        table.writerows(rows)
    print(work.name, {key: round(value, 5) for key,value in rows[-1].items()})


if __name__ == "__main__":
    main()
