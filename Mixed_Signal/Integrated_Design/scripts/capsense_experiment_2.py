#!/usr/bin/env python3
"""Experiment 2: Pressure sensitivity curves for several PMOS feedback-bank sizes.

Put this file AND capsense_experiment_1.py in the same directory.
Uses the same verified simulation/measurement methods from Experiment 1.
CSV-only output, no graphs or PNG files.

Default output:
  /home/shreyas/Desktop/Sec_7/Integrated_Design/experiment 2/

The 'CF_target_pF' entries are design targets from PMOS geometry scaling,
NOT extracted/effective capacitance measurements. Characterize the PMOS bank
separately before accepting these as physical 30/40/50/60pF capacitors.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from capsense_experiment_1 import find_netlist, pressure_points, run_cases

PROJECT = Path('/home/shreyas/Desktop/Sec_7/Integrated_Design')
EXP2_DIR = PROJECT / 'experiment 2'


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, help='Working Xschem-generated .spice deck')
    parser.add_argument('--out', type=Path, default=EXP2_DIR)
    parser.add_argument('--cf', type=float, nargs='+', default=[30, 40, 50, 60],
                        help='Target feedback capacitances (pF) via PMOS CFB_L geometry')
    parser.add_argument('--start', type=float, default=30)
    parser.add_argument('--stop', type=float, default=120)
    parser.add_argument('--step', type=float, default=5)
    parser.add_argument('--stop-us', type=float, default=1700)
    parser.add_argument('--timestep-ns', type=float, default=80)
    parser.add_argument('--sample-margin-us', type=float, default=2)
    parser.add_argument('--timeout', type=int, default=900)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        if any(cf <= 0 for cf in args.cf) or len(set(args.cf)) != len(args.cf):
            raise ValueError('CF values must be distinct and positive')
        netlist = find_netlist(args.netlist)
        pressures = pressure_points(args.start, args.stop, args.step)
        rows, summaries = run_cases(netlist, args.out.expanduser(), pressures,
                                    args.cf, args.stop_us, args.timestep_ns,
                                    args.sample_margin_us, args.dry_run, args.timeout)
        # Sort only complete, credible sweeps; flag TX > 5V rather than masking it.
        complete = [s for s in summaries if s.get('complete') and 'nonlinearity_pct_FS' in s]
        complete.sort(key=lambda s: (s['nonlinearity_pct_FS'],
                                     -abs(s['avg_pressure_sensitivity_mV_per_kPa'])))
        print(f'\nResults: {args.out.expanduser().resolve()}')
        if complete:
            top = complete[0]
            print(f'Lowest full-scale straight-line nonlinearity: CF target={top["CF_target_pF"]}pF; '
                  f'nonlinearity={top["nonlinearity_pct_FS"]:.4g}%, '
                  f'average sensitivity={top["avg_pressure_sensitivity_mV_per_kPa"]:.4g}mV/kPa')
            print('This is NOT a final design approval: also inspect TX overvoltage, drift, noise and ADC range.')
        else:
            print('No complete valid curves to rank; inspect failed rows/logs.')
        return 0 if any(r['status']=='OK' for r in rows) or args.dry_run else 2
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    sys.exit(main())

