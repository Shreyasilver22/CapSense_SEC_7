"""Measure integrated runs written by ngspice and plot the key waveforms."""
from pathlib import Path
import argparse
import csv
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CASES = {
    'ref_only': 'Buffer with ideal clock, 12/7 pF',
    'ref_hot': 'Buffer with ideal clock, hot 12/12 pF',
    'integrated_12_7': 'Fast TX recharge, nominal 12/7 pF',
    'integrated_hot': 'Untrimmed hot clock, 12/12 pF',
    'recharge_12_7': 'Slewed TX recharge, nominal 12/7 pF',
    'recharge_12_12': 'Slewed TX recharge, nominal 12/12 pF',
    'recharge_hot_12_12': 'Slewed TX recharge, hot trimmed 12/12 pF',
    'recharge_cold_12_7': 'Slewed TX recharge, cold trimmed 12/7 pF',
    'final_pr_12_7': 'Native clock and buffer, nominal 12/7 pF',
    'final_pr_12_12': 'Native clock and buffer, nominal 12/12 pF',
    'final_pr_hot_12_12': 'Hot clock with case-specific trim, 12/12 pF',
    'final_pr_cold_12_7': 'Cold clock with case-specific trim, 12/7 pF',
    'bypass_12_7': 'Native clock and buffered reference, nominal 12/7 pF',
    'bypass_12_12': 'Native clock and buffered reference, nominal 12/12 pF',
    'bypass_hot_12_12': 'Hot clock with case-specific trim, 12/12 pF',
    'bypass_cold_12_7': 'Cold clock with case-specific trim, 12/7 pF',
}

def crossings(t, wave, level, rising):
    y = wave-level
    if rising:
        mask = (y[:-1]<0)&(y[1:]>=0)
    else:
        mask = (y[:-1]>0)&(y[1:]<=0)
    i = np.flatnonzero(mask)
    return t[i] - y[i]*(t[i+1]-t[i])/(y[i+1]-y[i])

def timing_edge(t, wave, threshold, rising, first, last):
    edges = crossings(t, wave, threshold, rising)
    valid = edges[(edges>=first)&(edges<=last)]
    return float(valid[0]) if len(valid) else float('nan')

def metrics(data, name, description):
    t,clk,s1,rx,tx,txb,pre,tr,ref,master,op,on,sp,sn,hp,hn,txp,rxp,buf,clock,dd,drive=data.T
    t=t*1e6-200
    supply=max(clk)
    full=(t>=0)&(t<=100)
    transfer=(t>=40)&(t<=70)
    acquired=(t>=40)&(t<=81)
    end=timing_edge(t,tr,supply/2,False,50,99)
    start=timing_edge(t,tr,supply/2,True,45,99)
    tx10=timing_edge(t,tx,.1*supply,True,35,85)
    tx90=timing_edge(t,tx,.9*supply,True,35,88)
    cm=(op+on)/2
    incm=(sp+sn)/2
    held=hp-hn
    result=dict(case=name,description=description, reset_off_us=timing_edge(t,s1,supply/2,False,15,85),
                rx_on_us=timing_edge(t,rx,supply/2,True,15,85), 
                tx_10_us=tx10, tx_90_us=tx90, tx_slew_us=tx90-tx10,
                track_on_us=start, track_off_us=end, sample_at_81_mv=1e3*np.interp(81,t,held),
                actual_held_diff_mv=1e3*np.interp(end+1,t,held),
                held_cm_V=float(np.interp(end+1,t,(hp+hn)/2)),
                outcm_min_V=float(cm[transfer].min()), outcm_max_V=float(cm[transfer].max()),
                incm_min_V=float(incm[transfer].min()),
                ref_max_error_mv=1e3*float(np.max(abs(ref[full]-2.5))),
                ref_transfer_error_mv=1e3*float(np.max(abs(ref[acquired]-2.5))),
                peak_buffer_sink_ua=-1e6*float(np.min(drive[full])),
                clock_mW=1e3*supply*float(np.trapz(clock[full],t[full]))/100,
                buffer_mW=1e3*supply*float(np.trapz(buf[full],t[full]))/100,
                total_mW=-1e3*supply*float(np.trapz(dd[full],t[full]))/100)
    return result, (t, s1, rx, tx, pre, tr, ref, cm, held)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('work',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    traces={}
    rows=[]
    for name,description in CASES.items():
        job=args.work/name
        if not (job/'trace.dat').exists():
            continue
        log=(job/'run.log').read_text()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
            raise RuntimeError(f'Incomplete simulation {name}')
        trace=np.loadtxt(job/'trace.dat',skiprows=1)
        if trace[-1,0]<299.99e-6:
            raise RuntimeError(f'Incomplete waveform {name}')
        row,traces[name]=metrics(trace,name,description)
        rows.append(row)
    with (args.output/'results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    nominal=traces['bypass_12_7']
    fig, axes=plt.subplots(2,2,figsize=(12.5,7.5),layout='constrained')
    fig.suptitle('SCL08 readout with transistor-level timing and reference driver',fontweight='bold',fontsize=17)
    phase, ref, output_cm, held=axes.flat
    t, s1, rx, tx, pre, tr, *_=nominal
    for k,(name,values) in enumerate((('Reset / RX clamp',s1),('RX transfer',rx),
                                      ('TX discharge control',tx),('Hold precharge',pre),('Track',tr))):
        phase.plot(t,values/5+(4-k)*1.3,lw=1.5,label=name)
    phase.set(xlim=(36,96),title='Nominal timing from one 10 kHz clock',
              yticks=[0,1.3,2.6,3.9,5.2],
              yticklabels=['Track','Hold precharge','TX discharge','RX transfer','Reset / RX clamp'])
    for case,color in [('final_pr_12_7','#b45427'),('bypass_12_7','#2061a4'),
                       ('bypass_hot_12_12','#197b70'),('bypass_cold_12_7','#9167a8')]:
        if case not in traces:
            continue
        t, *_, vr, cm, hd = traces[case]
        label = 'Nominal without MOS bypass' if case=='final_pr_12_7' else CASES[case]
        ref.plot(t,1e3*(vr-2.5),color=color,label=label,lw=1.5)
        if case!='final_pr_12_7':
            output_cm.plot(t,cm,color=color,label=label,lw=1.5)
            held.plot(t,1e3*hd,color=color,label=label,lw=1.5)
    ref.set(xlim=(63,98),ylabel='Deviation from 2.5 V (mV)',title='Reference during precharge and reset')
    ref.legend(fontsize=7.6)
    output_cm.set(xlim=(40,70),ylabel='Voltage (V)',title='OTA output common-mode during transfer')
    held.set(xlim=(65,89),ylabel='Differential sample (mV)',title='Sample-and-hold response')
    for ax in axes.flat:
        ax.spines[['top','right']].set_visible(False)
        ax.set_xlabel('Time within cycle (µs)')
        ax.grid(alpha=.24)
    output_cm.axhline(2.5,ls='--',c='#828a94',lw=1)
    held.axvline(81,ls='--',c='#828a94',lw=1)
    fig.savefig(args.output/'integrated_waveforms.png',dpi=160)

if __name__=='__main__':
    main()
