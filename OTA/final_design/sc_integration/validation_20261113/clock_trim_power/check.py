"""Run clock calibration and integrated switched-capacitor checks."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import csv
import importlib.util
import re
import shutil
import subprocess

import numpy as np
from build import EDGES

HERE=Path(__file__).resolve().parent
PDK=Path.home()/'pdk/scl08/ngspice_models49'
SETTINGS = {
    0: ('wnwp',4.5,0,'best'),
    1: ('wnbp',5,27,'typ'),
    2: ('wnwp',5,27,'typ'),
    3: ('tntp',5,27,'typ'),
    4: ('bnbp',5,27,'typ'),
    5: ('bnwp',5.5,85,'worst'),
    6: ('bnwp',5,27,'typ'),
    7: ('tntp',5,27,'typ'),
}
CLOCK_VECTORS='v(clk) v(s1) v(rx) v(tx) v(txb) v(pre) v(tr) v(xclk.sensed) '+ ' '.join(f'v(xclk.q{k})' for k in EDGES)+' i(VDD)'
OLD = HERE.parent/'clock_reference_scl08'
spec=importlib.util.spec_from_file_location('existing_integration',OLD/'integrate.py')
integration=importlib.util.module_from_spec(spec)
spec.loader.exec_module(integration)


def pins(code,vdd):
    return '\n'.join(f'VTRIM{i} d{i} 0 {vdd if code&(1<<i) else 0}' for i in range(3))


def clock_deck(code, setting, duty):
    mos,vdd,temp,res=setting
    return f"""SCL08 switch-selected trim, standalone clock
.include "{PDK}/mos/{mos}49_5v"
.include "{PDK}/res/{res}/ppr"
.include blocks.spice
VDD vdd 0 {vdd}
VCLK clk 0 PULSE(0 {vdd} 0 1u 1u {duty-1}u 100u)
{pins(code,vdd)}
XCLK clk d0 d1 d2 vdd 0 s1 s1b rx rxb tx txb pre preb tr trb chg chgb phase_trim08
.temp {temp}
.options method=gear reltol=4e-4 vntol=3u abstol=1e-11
.save {CLOCK_VECTORS}
.control
set wr_vecnames
set wr_singlescale
tran 120n 103u 0 120n
wrdata trace.dat {CLOCK_VECTORS}
quit
.endc
.end
"""


def integrated_deck(code, setting, cn, clock, bias=False):
    mos,vdd,temp,res=setting
    text=integration.make_deck(supply=vdd,temp=temp,model=mos,resistor=res,cp=12,cn=cn,
                               physical_clock=clock,physical_reference=True,bypass_units=150)
    text=text.replace('XCLK clk10k clk_vdd','XCLK clk10k d0 d1 d2 clk_vdd').replace('phase08','phase_trim08')
    text=text.replace('XREF ref_src vref_driven buf_vdd','XREF ref_src vref_driven d2 buf_vdd')
    text=text.replace('VCLKDD vdd clk_vdd 0','VCLKDD vdd clk_vdd 0\n'+pins(code,vdd))
    text=text.replace('reltol=1e-4 vntol=1e-8 abstol=1e-12','reltol=4e-4 vntol=3u abstol=1e-11')
    vectors=integration.VECTORS
    if bias:
        text=re.sub(r'(?m)^(VBN|VBP|IREF) .*\n','',text)
        wiring=('.include ota_bias.spice\nVBIASDD vdd bias_vdd 0\n'
                'XB ref_src bias_vdd 0 vbn vbp bias_src ota_bias08\nVIREF bias_src bias 0\n')
        text=text.replace('.control',wiring+'.control')
        vectors+=' v(vbn) v(vbp) i(VIREF) i(VBIASDD)'
        text=text.replace(integration.VECTORS,vectors)
    text=text.replace('.control',f'.save {vectors}\n.control')
    return text.replace('50n 300u 0 50n','120n 103u 0 120n')


def crossing(t,y,threshold,direction,earliest=12):
    sign=(y-threshold)*direction
    inds=np.flatnonzero((sign[:-1]<0)&(sign[1:]>=0)&(t[:-1]>earliest)&(t[:-1]<99.95))
    if not len(inds):
        return float('nan')
    i=inds[0]
    return float(t[i]-sign[i]*(t[i+1]-t[i])/(sign[i+1]-sign[i]))


def measure(a,setting,clock_only):
    _,vdd,_,_=setting
    t=a[:,0]*1e6-(100 if a[-1,0]>150e-6 else 0)
    use=(t>=0)&(t<=100)
    at=(t>=40)&(t<=70)
    reset,rx,tx,pre,tr=a[:,[2,3,4,6,7]].T
    cm=(a[:,10]+a[:,11])/2
    ton=crossing(t,tr,vdd/2,1)
    toff=crossing(t,tr,vdd/2,-1,ton if np.isfinite(ton) else 70)
    r=dict(reset_off_us=crossing(t,reset,vdd/2,-1), rx_on_us=crossing(t,rx,vdd/2,1),
           tx10_us=crossing(t,tx,.1*vdd,1), tx90_us=crossing(t,tx,.9*vdd,1),
           pre_off_us=crossing(t,pre,vdd/2,-1),track_on_us=ton,track_off_us=toff,
           rx_off_us=crossing(t,rx,vdd/2,-1,50))
    def avg(i):
        return 1e3*vdd*np.trapz(i[use],t[use])/100
    if clock_only:
        r['clock_mw']=avg(-a[:,-1])
        for i,(edge,sgn) in enumerate(zip(EDGES,(-1,1,1,-1,1,-1,-1)),9):
            r[f'q{edge}_us']=crossing(t,a[:,i],vdd/2,sgn,29 if edge==90 else 12)
    else:
        r.update(clock_mw=avg(a[:,19]),buffer_mw=avg(a[:,18]),total_mw=avg(-a[:,20]),
                 peak_ref_mv=float(np.max(abs(a[use,8]-2.5))*1e3),
                 transfer_ref_mv=float(np.max(abs(a[at,8]-2.5))*1e3),
                 min_cm_V=float(np.min(cm[at])),max_cm_V=float(np.max(cm[at])),
                 held_diff_mV=float(1e3*np.interp(81,t,a[:,14]-a[:,15])),
                 held_cm_V=float(np.interp(81,t,(a[:,14]+a[:,15])/2)))
        if a.shape[1]>22:
            r.update(vbn_V=float(np.interp(81,t,a[:,22])),vbp_V=float(np.interp(81,t,a[:,23])),
                     iref_uA=float(np.interp(81,t,a[:,24])*1e6),bias_mw=avg(a[:,25]))
    return r


def run(a, name, code, setting, data, only):
    dst=a.work/name
    dst.mkdir(exist_ok=True,parents=True)
    shutil.copyfile(a.blocks,dst/'blocks.spice')
    if '.include ota_bias.spice' in data:
        shutil.copyfile(HERE/'ota_bias.spice',dst/'ota_bias.spice')
    (dst/'run.cir').write_text(data)
    result=dict(case=name,code=code,mos=setting[0],vdd=setting[1],temp=setting[2])
    try:
        subprocess.run(['ngspice','-b','-o','run.log','run.cir'],cwd=dst,
                       capture_output=True,check=True,timeout=110)
        log=(dst/'run.log').read_text()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
            raise ValueError('ngspice run stopped')
        trace=np.loadtxt(dst/'trace.dat',skiprows=1)
        stop_us=float(re.search(r'(?m)^tran \S+ ([0-9.]+)u',data)[1])
        if trace[-1,0]<(stop_us-.01)*1e-6:
            raise ValueError('incomplete transient')
        result.update(measure(trace,setting,only),status='ok')
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        result['status']=str(exc)
    print(name,result['status'],flush=True)
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('group',choices=('clock','integrated','ref-only','duty','bias'))
    p.add_argument('work',type=Path)
    p.add_argument('blocks',type=Path)
    p.add_argument('--jobs',type=int,default=6)
    p.add_argument('--codes',type=int,nargs='+',choices=tuple(SETTINGS))
    p.add_argument('--cycles',type=int,choices=(1,2),default=1)
    p.add_argument('--klu',action='store_true')
    a=p.parse_args()
    if a.group=='clock':
        cases=[(f'clock{k}',k,s,clock_deck(k,s,50),True) for k,s in SETTINGS.items()]
    elif a.group=='duty':
        cases=[(f'duty{duty}',3,SETTINGS[3], clock_deck(3,SETTINGS[3],duty),True) for duty in (40,60)]
    elif a.group=='bias':
        cases=[(f'bias{k}_{cn}',k,SETTINGS[k],integrated_deck(k,SETTINGS[k],cn,True,True),False)
               for k,cn in ((0,7),(3,7),(5,12))]
    else:
        clock=a.group=='integrated'
        cases=[(f'{a.group}{k}_{cn}',k,SETTINGS[k],integrated_deck(k,SETTINGS[k],cn,clock),False)
               for k,cn in ((3,7),(3,12),(5,12),(5,7),(0,7),(1,7),(2,7),(4,7),(6,7))]
    selected=[]
    for name,code,setting,deck,only in cases:
        if a.codes and code not in a.codes:
            continue
        if a.cycles==2:
            deck=deck.replace('120n 103u 0 120n','120n 203u 0 120n')
        if a.klu:
            deck=deck.replace('.control','.control\noption klu')
        selected.append((name,code,setting,deck,only))
    with ThreadPoolExecutor(a.jobs) as ex:
        results=list(ex.map(lambda case:run(a,*case), selected))
    fields=list(dict.fromkeys(k for r in results for k in r))
    with (a.work/f'{a.group}.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

if __name__=='__main__':
    main()
