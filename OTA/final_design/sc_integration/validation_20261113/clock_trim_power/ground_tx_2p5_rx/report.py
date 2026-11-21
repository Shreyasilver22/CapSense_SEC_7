"""Publish the selected-case comparison, local slopes and nominal waveforms."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from compare import HERE, PAIRS, case_folder, measure, raw_trace, save


def load(path):
    with path.open() as file:
        rows = list(csv.DictReader(file))
    if any(r['status'] != 'ok' for r in rows):
        raise ValueError(f'Unsuccessful simulations in {path}')
    return {(float(r['tx_discharge_V']), float(r['cp_pF']), float(r['cn_pF'])): r
            for r in rows}


def plot(work):
    fig, axes = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True, layout='constrained')
    fig.suptitle('TX discharge comparison with RX precharge at 2.5 V',
                 fontweight='bold', fontsize=17, color='#132840')
    for tx, color in ((0, '#086e84'), (2.5, '#ad4b24')):
        for ax, (cp, cn) in zip(axes, ((15, 15), (12, 7))):
            data = raw_trace(case_folder(work, tx, cp, cn, 10) / 'trace.raw')
            t = data['time'] * 1e6
            label = f'TX {tx:g} V'
            if cp == cn:
                voltage = (data['v(sump)'] + data['v(sumn)']) / 2
                ax.plot(t, voltage, color=color, label=label, linewidth=1.4)
            else:
                live = (data['v(outp)'] - data['v(outn)']) * 1e3
                hold = (data['v(holdp)'] - data['v(holdn)']) * 1e3
                ax.plot(t, live, color=color, label=label + ' live', linewidth=1.4)
                ax.plot(t, hold, color=color, label=label + ' held', linewidth=1.2,
                        linestyle='--')
    axes[0].axhline(1.5, linestyle=':', linewidth=.9, color='#657283',
                    label='1.5 V design point')
    axes[0].set(title='Balanced sensors at 15/15 pF', ylabel='OTA input common-mode (V)',
                xlim=(40, 89))
    axes[0].legend(loc='lower right')
    axes[1].set(title='Mismatched sensors at 12/7 pF', ylabel='Differential output (mV)',
                xlabel='Time (µs)')
    axes[1].legend(loc='lower right', ncol=2)
    for ax in axes:
        ax.axvline(81, linestyle=':', color='#657283', linewidth=.9)
        ax.grid(axis='y', alpha=.18)
    fig.savefig(HERE / 'tx_ground_comparison.png', dpi=180)
    fig.savefig(HERE / 'tx_ground_comparison.pdf')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    work = parser.parse_args().work
    nominal = load(work / 'nominal.csv')
    fine = load(work / 'refine.csv')
    perturbed = load(work / 'sensitivity.csv')
    assert len(nominal) == 12 and len(fine) == 8 and len(perturbed) == 48
    rows = []
    for tx in (0, 2.5):
        for cp, cn in PAIRS:
            key = (tx, cp, cn)
            row = (fine.get(key) or nominal[key]).copy()
            if key not in fine:
                row.update(measure(case_folder(work, tx, cp, cn, 40) / 'trace.raw', 5))
            y = lambda p, n: float(perturbed[tx, round(p, 2), round(n, 2)]['held_diff_mV'])
            slope_p = (y(cp + .1, cn) - y(cp - .1, cn)) / .2
            slope_n = (y(cp, cn + .1) - y(cp, cn - .1)) / .2
            row.update(dVheld_dCP_mV_per_pF=slope_p, dVheld_dCN_mV_per_pF=slope_n,
                       fixed_sum_dVheld_dCPminusCN_mV_per_pF=(slope_p - slope_n) / 2)
            rows.append(row)
    save(HERE / 'nominal_results.csv', rows)
    save(HERE / 'sensitivity_runs.csv', list(perturbed.values()))
    for corner in ('cold', 'hot'):
        path = work / f'nominal_{corner}.csv'
        if path.is_file():
            with path.open() as file:
                corner_rows = list(csv.DictReader(file))
            retries = work / 'hot_retries.csv'
            if corner == 'hot' and retries.is_file():
                with retries.open() as file:
                    retry_rows = list(csv.DictReader(file))
                success = {(r['tx_discharge_V'], r['cp_pF'], r['cn_pF']): r
                           for r in reversed(retry_rows) if r['status'] == 'ok'}
                corner_rows = [success.get((r['tx_discharge_V'], r['cp_pF'], r['cn_pF']), r)
                               if r['status'] != 'ok' else r for r in corner_rows]
                save(HERE / 'hot_solver_checks.csv', retry_rows)
            for row in corner_rows:
                row.setdefault('solver', 'klu_trap')
            save(HERE / f'{corner}_screen.csv', corner_rows)
    plot(work)


if __name__ == '__main__':
    main()
