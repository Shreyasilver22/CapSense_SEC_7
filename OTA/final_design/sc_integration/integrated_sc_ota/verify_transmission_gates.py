"""Prove the integrated SC circuit uses the SCL08 MOS transmission gates."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import csv
import re
import subprocess

import numpy as np

from verify import ROOT, read_raw

OUT = ROOT/'transmission_gate_verification'
SUPPORT = ROOT/'bench_support_schematic.spice'
SWITCH_NAMES = ('SENSE','SRESET','CHARGE','RRESET','XFER','FBRESET')
PRESSURE_CAP_VALUES = (7.82, 10.5, 11.79)
CLOCKS = ('phi1','phi1b','phi2','phi2b','phit','phitb')


def run_spice(circuit, logfile, raw=None, cwd=ROOT):
    args = ['ngspice','-b','-o',str(logfile)]
    if raw is not None:
        args += ['-r',str(raw)]
    p = subprocess.run([*args,str(circuit)],cwd=cwd,capture_output=True,text=True,timeout=100)
    p.check_returncode()
    if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',logfile.read_text()):
        raise RuntimeError(f'Incomplete simulation. See {logfile}')


def csv_write(path, rows):
    with path.open('w',newline='') as file:
        w = csv.DictWriter(file,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def characterize_gate(macro, pdk_include):
    # Bias both terminals around the same voltage and apply a 10 mV differential.
    deck = OUT/'tg_dc.cir'
    deck.write_text(f"""SCL08 transmission gate DC test at 27 C
{pdk_include}
{macro}
VDD vdd 0 5
VBIAS vcm 0 0
VA a vcm 5m
VB b vcm -5m
VP phi 0 5
VPB phib 0 0
XTEST a b phi phib vdd 0 corrected_tg
.temp 27
.control
set wr_singlescale
set wr_vecnames
dc VBIAS .25 4.75 .25
wrdata tg_on.dat i(VA) i(VB)
alter VP 0
alter VPB 5
dc VBIAS .25 4.75 .25
wrdata tg_off.dat i(VA) i(VB)
quit
.endc
.end
""")
    (OUT/'.spiceinit').write_text((ROOT/'.spiceinit').read_text())
    run_spice(deck,OUT/'tg_dc.log',cwd=OUT)
    on,off = (np.loadtxt(OUT/f'tg_{p}.dat',skiprows=1) for p in ('on','off'))
    assert np.allclose(on[:,0],off[:,0])
    rows=[]
    for (v,ia,ib),(_,ia_off,ib_off) in zip(on,off):
        rows.append(dict(common_mode_V=v,r_on_ohm=0.01/abs((ia-ib)/2),
                         off_terminal_A_pA=1e12*ia_off,off_terminal_B_pA=1e12*ib_off))
    csv_write(OUT/'tg_dc_characterization.csv',rows)
    print('27 C DC Ron at 2.5 V and bracketing tested min/max:',rows[9]['r_on_ohm'],
          min(x['r_on_ohm'] for x in rows), max(x['r_on_ohm'] for x in rows),flush=True)
    return rows


def integrated(netlist, cp):
    circuit=OUT/f'cg_{cp:g}.spice'
    working, count = re.subn(r'(?im)^(CMEMP\s+\S+\s+\S+\s+)\S+',
                             lambda m:m[1]+f'{cp:g}p',netlist)
    if count!=1:
        raise ValueError('Expected a single P sensor capacitance')
    circuit.write_text(working)
    raw=OUT/f'cg_{cp:g}.raw'
    run_spice(circuit,circuit.with_suffix('.log'),raw=raw)
    w=read_raw(raw)
    t=w['time']*1e6
    val=lambda a,b:float(np.interp(a,t,w[f'v({b})']))
    sample=380
    window=(t>=340)&(t<=380)
    in_cm=(w['v(sump)']+w['v(sumn)'])/2
    diff=(w['v(outp)']-w['v(outn)'])*1000
    ds=np.interp([80,180,280,380],t,diff)
    row=dict(cp_pF=cp,cn_pF=10,diff_at_sample_mV=ds[-1],cycle_to_cycle_spread_uV=np.ptp(ds)*1000,
             output_cm_at_sample_V=(val(sample,'outp')+val(sample,'outn'))/2,
             input_cm_at_sample_V=np.interp(sample,t,in_cm),input_cm_min_V=min(in_cm[window]))
    for name in CLOCKS:
        row[f'{name}_at_sample_V']=val(sample,name)
    print(row,flush=True)
    return row


def main():
    OUT.mkdir(exist_ok=True)
    subprocess.run(['xschem','--rcfile',str(ROOT/'xschemrc'),'-n','-x','-q','-o',str(OUT),
                    '-l',str(OUT/'xschem.log'),'sc_ota_integrated.sch'],
                   cwd=ROOT,check=True,timeout=30)
    original=(OUT/'sc_ota_integrated.spice').read_text()
    actual={r.split()[0] for r in original.splitlines()
            if r.strip().endswith('corrected_tg') and r.startswith('X')}
    expected={f'X{name}{suffix}' for name in SWITCH_NAMES for suffix in 'PN'}
    if actual!=expected or re.search(r'(?im)^S\S+\s',original):
        raise ValueError('Unexpected switching devices in integrated netlist')
    support = SUPPORT.read_text()
    macro=re.search(r'(?ims)^\.subckt corrected_tg\b.*?^\.ends corrected_tg[^\n]*',support)[0]
    pdk_include=re.search(r'(?m)^\.include .*?/mos/.*$',support)[0]
    if len(re.findall(r'(?im)^M[N|P]\s',macro))!=2:
        raise ValueError('Invalid transmission gate MOS count')
    if re.search(r'(?im)^\.model\s+\S+\s+SW\b',support):
        raise ValueError('An ideal switch model appeared in the bench')
    print(f'Verified {len(actual)} complementary-MOS transmission gates.',flush=True)
    extra = re.sub(r'(?m)^\.save [^\n]*',
                   lambda m:m[0]+' v(phi1b) v(phi2b) v(phitb)',support)
    tmp_support=OUT/'bench_support_tg.spice'
    tmp_support.write_text(extra)
    netlist=original.replace('.include bench_support_schematic.spice',f'.include "{tmp_support}"')
    with ThreadPoolExecutor(4) as pool:
        dc = pool.submit(characterize_gate,macro,pdk_include)
        rows = list(pool.map(lambda cp: integrated(netlist,cp),PRESSURE_CAP_VALUES))
        dc.result()
    csv_write(OUT/'integrated_tg_sweep.csv',rows)
    assert rows[0]['diff_at_sample_mV']<rows[1]['diff_at_sample_mV']<rows[2]['diff_at_sample_mV']
    slope=(rows[-1]['diff_at_sample_mV']-rows[0]['diff_at_sample_mV'])/(PRESSURE_CAP_VALUES[-1]-PRESSURE_CAP_VALUES[0])
    print(f'Transmission-gate integrated slope: {slope:.5f} mV/pF',flush=True)


if __name__=='__main__':
    main()

