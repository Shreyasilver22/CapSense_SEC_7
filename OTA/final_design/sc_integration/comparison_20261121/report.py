"""Summarize ngspice outputs and render the comparisons for the four OTA models."""
from pathlib import Path
import csv
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from compare import ROOT, OTAS, Case, read_raw, save

COLORS = {'telescopic':'#5e9493','boosted':'#bc8669',
          'telescopic_C':'#007676','boosted_C':'#ad4514'}
LABELS = {'telescopic':'Telescopic schematic','boosted':'Gain-boosted schematic',
          'telescopic_C':'Telescopic extracted C','boosted_C':'Gain-boosted extracted C'}

def read(name):
    p = ROOT/(name+'.csv')
    if not p.is_file():
        return []
    out = list(csv.DictReader(p.open()))
    for r in out:
        if r.get('status') == 'ok' and float(r['readout_mW']) < .1:
            for key in ('readout_mW','ota_uW','clock_mW','refbuf_mW'):
                r[key] = str(float(r[key])*1000)
    return out


def get(rows,key):
    return np.asarray([float(r[key]) for r in rows])


def pressure_table(all_data):
    results = []
    corners = ('typ','cold','hot')
    for ota in OTAS:
        a = [sorted([r for r in all_data if (r['ota'],r['corner'],r['status'])==
                     (ota,c,'ok')],key=lambda r: int(r['pressure_kPa'])) for c in corners]
        nom = a[0]
        if not nom:
            continue
        pressure, y = get(nom,'pressure_kPa'),get(nom,'held_diff_mV')
        monotonic = bool(np.all(np.diff(y)>0) or np.all(np.diff(y)<0))
        sensitivity = float((y[-1]-y[0])/(pressure[-1]-pressure[0]))
        cm = get(nom,'held_cm_V')
        for corner,rows in zip(corners,a):
            if not rows:
                continue
            v = get(rows,'held_diff_mV')
            p = get(rows,'pressure_kPa')
            worst = float('nan')
            if monotonic:
                xp, yp = (y,pressure) if sensitivity>0 else (y[::-1],pressure[::-1])
                pred = np.interp(v,xp,yp)
                lo,hi=v<xp[0],v>xp[-1]
                pred[lo]=yp[0]+(v[lo]-xp[0])*(yp[1]-yp[0])/(xp[1]-xp[0])
                pred[hi]=yp[-1]+(v[hi]-xp[-1])*(yp[-1]-yp[-2])/(xp[-1]-xp[-2])
                worst = float(np.max(abs(pred-p)))
            slack = get(rows,'settling_slack_us')
            i100 = next((r for r in rows if r['pressure_kPa']=='100'),{})
            valid = int(np.count_nonzero(np.isfinite(slack)))
            idx = np.isfinite(slack)
            results.append(dict(ota=ota,corner=corner,samples=len(rows),settled_count=valid,
                  monotonic=bool(np.all(np.diff(v)>0) or np.all(np.diff(v)<0)),
                  differential_first_mV=v[0],differential_last_mV=v[-1],
                  sensitivity_avg_mV_kPa=(v[-1]-v[0])/(p[-1]-p[0]),
                  min_slack_us=min(slack[idx]) if valid else float('nan'),
                  max_held_cm_error_mV=np.max(abs(get(rows,'held_cm_V')-2.5))*1e3,
                  worst_lut_error_kPa=worst,held_100kPa_mV=i100.get('held_diff_mV'),
                  hold_cm_100kPa_V=i100.get('held_cm_V'),ota_power_100kPa_uW=i100.get('ota_uW'),
                  total_power_100kPa_mW=i100.get('readout_mW')))
    return results


def plot(all_data):
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(2,2,figsize=(11,7.4),layout='constrained')
    pressure, time, common, physical = axes.ravel()
    for ota in OTAS:
        n = sorted([r for r in all_data if (r['ota'],r['corner'],r['status'])==(ota,'typ','ok')],
                   key=lambda r:int(r['pressure_kPa']))
        if not n:
            continue
        pressure.plot(get(n,'pressure_kPa'),get(n,'held_diff_mV'),color=COLORS[ota],
                      marker='o',markersize=3,linestyle='-' if '_C' in ota else '--',label=LABELS[ota])
        case = Case(ota,'typ',100)
        data = read_raw(ROOT/'benches'/case.name/'trace.raw',case)
        t = data['time']*1e6
        mask = (t>=42)&(t<=92)
        p,n = data['v(pinp)'],data['v(pinn)']
        active_p,active_n = data['v(outp)'],data['v(outn)']
        if ota in ('telescopic_C','boosted_C'):
            time.plot(t[mask],(active_p[mask]-active_n[mask])*1e3,color=COLORS[ota],
                      alpha=.5,lw=1,label=LABELS[ota]+' live')
            time.plot(t[mask],(p[mask]-n[mask])*1e3,color=COLORS[ota],label=LABELS[ota]+' held')
            common.plot(t[mask],(p[mask]+n[mask])/2,color=COLORS[ota],label=LABELS[ota])
    pressure.set(title='Held differential voltage versus absolute pressure',
                 xlabel='Pressure (kPa)',ylabel='Held differential (mV)')
    pressure.legend(loc='upper left',fontsize=8)
    for ax in (time,common):
        ax.axvspan(69.8,80,color='#bbc5ce',alpha=.32,label='Track window')
        ax.axvline(81, color='#384654',linestyle=':',lw=1)
        ax.set_xlabel('Time into 10 kHz cycle (µs)')
    time.set(title='Extracted OTAs at 100 kPa',ylabel='Differential output (mV)')
    time.legend(loc='best',fontsize=7,ncols=2)
    common.axhline(2.5,linestyle='--',lw=1,color='#343a40')
    common.set(title='Common-mode at the external pins',ylabel='Pin common-mode (V)')
    common.legend(loc='best',fontsize=8)
    path=ROOT/'boosted_layout/verification/geometry_summary.json'
    geom=json.loads(path.read_text())
    areas=[1.2966137152,geom['area_mm2']]
    bars=physical.barh(['Telescopic','Gain-boosted'],areas,
                       color=[COLORS['telescopic_C'],COLORS['boosted_C']])
    physical.bar_label(bars,fmt='%.2f mm²',padding=5,fontsize=10)
    physical.set(xlim=(0,3.35),title='OTA layout bounding area',xlabel='Bounding area (mm²)')
    physical.invert_yaxis()
    for ax in axes.ravel():
        ax.grid(alpha=.2,axis='x' if ax is physical else 'both')
        ax.set_axisbelow(True)
    fig.suptitle('SCB10H readout with SCL08 OTA candidates',fontsize=15,fontweight='bold')
    fig.savefig(ROOT/'integration_comparison.png',dpi=180)
    fig.savefig(ROOT/'integration_comparison.pdf')
    plt.close(fig)


def main():
    base = [r for f in ('nominal','nominal_boosted_C','pvt','pvt_boosted_C') for r in read(f)]
    summary = pressure_table(base)
    save(ROOT/'pressure_summary.csv',summary)
    stress = [r for f in ('stress','stress_boosted_C','fine','fine_boosted_C','pex_diagnostics') for r in read(f)]
    all_data = list({r['case']:r for r in base+stress}.values())
    if all_data:
        save(ROOT/'all_results.csv',all_data)
        print('Total completed cases',sum(r['status']=='ok' for r in all_data),'of',len(all_data))
    plot(base)
    for r in summary:
        print(r['ota'],r['corner'],f"{r['settled_count']}/{r['samples']} settled",
              '100 kPa:',r['held_100kPa_mV'],r['hold_cm_100kPa_V'],
              'minimum slack',r['min_slack_us'],'worst LUT error',r['worst_lut_error_kPa'],
              'slope avg',r['sensitivity_avg_mV_kPa'])


if __name__=='__main__':
    main()

