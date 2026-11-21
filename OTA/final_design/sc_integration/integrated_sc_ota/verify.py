"""Netlist the editable schematic and run a nominal capacitance sweep with ngspice."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import csv
import re
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT/'results'
TOP = 'sc_ota_integrated'


def read_raw(path):
    header, binary = path.read_bytes().split(b'Binary:\n',1)
    n = int(re.search(rb'No\. Points:\s*(\d+)',header)[1])
    keys = [k.decode().lower() for k in re.findall(rb'(?m)^\s*\d+\s+(\S+)\s+\S+[^\n]*$',header)]
    wave = np.frombuffer(binary,dtype='<f8').reshape(n,len(keys))
    if wave[-1,0] < 394.99e-6 or not np.isfinite(wave).all():
        raise ValueError(f'Incomplete or invalid waveform {path}')
    return dict(zip(keys,wave.T))


def simulation(netlist, cp):
    name = f'cp_{cp:g}'
    path = RESULTS/f'{name}.spice'
    netlist, n = re.subn(r'(?im)^(CMEMP\s+\S+\s+\S+\s+)\S+',lambda m: m[1]+f'{cp:g}p',netlist)
    if n!=1:
        raise ValueError('Could not locate a unique P-side sensor capacitor')
    path.write_text(netlist)
    log, raw = RESULTS/f'{name}.log', RESULTS/f'{name}.raw'
    subprocess.run(['ngspice','-b','-r',str(raw),'-o',str(log),str(path)],cwd=ROOT,
                   check=True,timeout=120,stdout=subprocess.DEVNULL)
    if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log.read_text()):
        raise RuntimeError(f'Simulation did not complete. See {log}.')
    w = read_raw(raw)
    t = w['time']*1e6
    diff = 1e3*(w['v(outp)']-w['v(outn)'])
    cm_in = (w['v(sump)']+w['v(sumn)'])/2
    cm_out = (w['v(outp)']+w['v(outn)'])/2
    sample = np.interp([80,180,280,380],t,diff)
    pulse=(t>=340)&(t<=380)
    row = dict(cp_pF=cp, cn_pF=10, diff_cycle1_mV=sample[0],diff_cycle4_mV=sample[-1],
               cycle_spread_mV=np.ptp(sample), input_cm_sample_V=np.interp(380,t,cm_in),
               input_cm_min_V=np.min(cm_in[pulse]),output_cm_sample_V=np.interp(380,t,cm_out))
    print(row,flush=True)
    return row


def main():
    RESULTS.mkdir(exist_ok=True)
    subprocess.run(['xschem','--rcfile',str(ROOT/'xschemrc'),'-n','-x','-q',
                    '-l',str(RESULTS/'xschem.log'),f'{TOP}.sch'],cwd=ROOT,check=True,timeout=40)
    netlist = (RESULTS/f'{TOP}.spice').read_text()
    expected = ['.subckt ota_core INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP',
                'XOTA sumn sump outp outn ota_vdd 0 bias vref vbn vbp ota_core',
                'XSENSEP sensp txp phi2 phi2b vdd 0 corrected_tg',
                'XSENSEN sensn txn phi2 phi2b vdd 0 corrected_tg',
                'XSRESETP sensp 0 phi1 phi1b vdd 0 corrected_tg',
                'XSRESETN 0 sensn phi1 phi1b vdd 0 corrected_tg',
                'XCFP sump outp corrected_pmos_bank','XCFN sumn outn corrected_pmos_bank']
    for entry in expected:
        if entry not in netlist.splitlines():
            raise ValueError(f'Missing schematic connection {entry}')
    with ThreadPoolExecutor(4) as pool:
        rows = list(pool.map(lambda c: simulation(netlist,c),(7.82,10,10.5,11.79)))
    with (RESULTS/'schematic_sweep.csv').open('w',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    out=[r['diff_cycle4_mV'] for r in rows]
    if not all(a<b for a,b in zip(out,out[1:])):
        raise ValueError('Capacitance transfer is not monotonic')
    if any(r['cycle_spread_mV']>.05 for r in rows):
        raise ValueError('Clock-cycle samples differ by more than 50 uV')
    print(f'Endpoint sensitivity: {(out[-1]-out[0])/(rows[-1]["cp_pF"]-rows[0]["cp_pF"]):.5f} mV/pF')


if __name__=='__main__':
    main()

