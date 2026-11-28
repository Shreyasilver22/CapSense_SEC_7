"""Matched sensitivity transients for the integrated SCL08 readout."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_icm import DEFAULT_CELL, ROOT, instantiate, measure, read_raw, set_feedback_bank
from waveform_checks import first_settled, write_table

HERE = Path(__file__).resolve().parent
SCHEM = ROOT / "schematic" / "netlist"
MODELS = Path(os.environ["SCL08_MODELS"])
CELL = DEFAULT_CELL

@dataclass(frozen=True)
class Case:
    key: str
    cp: float
    fb: int
    schematic: bool = False
    corner: str = 'typ'


def stage(case):
    if case.schematic:
        directory = HERE / "runs" / case.key
        directory.mkdir(parents=True, exist_ok=True)
        text = (SCHEM / "sc_vcr_input_cm_scl08.spice").read_text()
        text, count = re.subn(r"(?mi)^(CMEMP 0 sensp )\S+", rf"\g<1>{case.cp:g}p", text)
        if not count:
            text, count = re.subn(r"(?mi)^(CMEMP sensp 0 )\S+", rf"\g<1>{case.cp:g}p", text)
        assert count == 1
        (directory / "bench.cir").write_text(text)
        shutil.copyfile(SCHEM / ".spiceinit",directory / ".spiceinit")
        support = (SCHEM / "bench_support.spice").read_text()
        (directory / "bench_support.spice").write_text(set_feedback_bank(support,case.fb))
        return directory, 12, 0
    cycles = 10 if case.corner == 'typ' else 13
    prepared = SimpleNamespace(name=case.key, models_dir=MODELS, corner=case.corner, cycles=cycles,
                                mode="mos", cp=case.cp, cn=10, tap=390, mi=9, bank=40, gear=False, cell=CELL,
                                feedback_units=case.fb)
    directory, delay, _ = instantiate(prepared)
    return directory, cycles, delay


def simulate(case):
    work, cycles, delay = stage(case)
    with (work / "console.log").open("w") as console:
        command = ["ngspice", "-b", "-r", "trace.raw", "-o", "run.log", "bench.cir"]
        subprocess.run(command, cwd=work, stdout=console, stderr=subprocess.STDOUT, check=True)
    wave = read_raw(work/"trace.raw")
    end_us = wave["time"][-1]*1e6
    if abs(end_us - (cycles*100-5+delay)) > 0.01:
        raise RuntimeError(f"{case.key}: transient ended at {end_us:g} us. {work/'run.log'}")
    rows = measure(wave,delay,cycles,{"typ":5,"cold":4.5,"hot":5.5}[case.corner])
    write_table(work/"samples.csv",rows)
    point = dict(case=case.key,corner=case.corner, cp_pF=case.cp, cn_pF=10, fb_per_branch=case.fb,
                 settled_cycle=first_settled(rows), **rows[-1])
    print(point, flush=True)
    return point


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage",choices=("nominal","candidate"),default="nominal")
    args=parser.parse_args()
    endpoints=(("low",7.82),("high",11.79))
    if args.stage=="nominal":
        cases = [Case(f"int_xschem60_{name}",cp,60,True) for name,cp in endpoints]
        for count in (60,48,40):
            cases += [Case(f"int_flat{count}_{name}",cp,count) for name,cp in endpoints]
        output="new_matched_points.csv"
    else:
        cases = [Case(f"int_xschem40_{name}",cp,40,True) for name,cp in endpoints]
        for corner in ("cold","hot"):
            cases += [Case(f"int_{corner}40_{name}",cp,40,False,corner) for name,cp in endpoints]
        output="candidate_corner_points.csv"
    with ThreadPoolExecutor(max_workers=min(6,len(cases))) as pool:
        points=list(pool.map(simulate,cases))
    write_table(HERE/output,points)


if __name__ == "__main__":
    main()
