"""Characterize the final SCL08 OTA versus input common-mode."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import csv
import re
import subprocess

import numpy as np

OTA = Path.home() / 'final year project/ota/final_design'
PDK = Path.home() / 'pdk/scl08/ngspice_models49'
DEVICES = {
    'input': ('m1007', 'm1059'),
    'n_cascode': ('m1015', 'm1033'),
    'p_cascode': ('m1041', 'm1042'),
    'tail': ('m1039',),
    'p_load': ('m1008', 'm1045'),
    'reference_mirror': ('m1053',),
}
DEV = [d for devices in DEVICES.values() for d in devices]
OP = 'v(inp) v(inn) v(op) v(om) v(bn) i(VDD)'
COLS = tuple(f'@m.xota.{d}[{p}]' for d in DEV for p in ('vds', 'vdsat', 'id', 'vgs'))
NODE = 'v(op) v(om) v(inp) v(inn) i(VDD) v(cmd)'
MARGIN_COLUMNS = ' '.join(f'@m.xota.{d}[{p}]' for d in DEV for p in ('vds','vdsat'))


def fixture(vcm, iref, model, vdd, temperature, rpp):
    return f"""SCL08 extracted-capacitance OTA input common-mode characterization
.include "{PDK}/mos/{model}49_5v"
.include "{PDK}/res/{rpp}/ppr"
.include "{OTA}/models/ota_cm2p5_C.spice"
.temp {temperature}
.options reltol=1e-5 vntol=1e-8 abstol=1e-12 method=gear maxord=2
VDD vdd 0 {vdd}
IREF vdd bn {iref}u
VCM vcm 0 2.5
VBN vbn 0 3
VBP vbp vdd -2.2
XOTA inp inn op om vdd 0 bn vcm vbn vbp ota_telescopic_cm2p5
CLP op 0 5p
CLM om 0 5p
EOD od 0 op om 1
VICM icm 0 {vcm}
"""


def header():
    return '.control\nset wr_singlescale\nset wr_vecnames\nset numdgt=12\n'


def ac_deck(base):
    return base+f"""VCMD cmd 0 dc 0 ac 1
EIP inp icm cmd fb 0.5
EIM inn icm fb cmd 0.5
LDC od fb 1e12
CAC fb 0 1e12
{header()}op
wrdata op.dat {OP} {' '.join(COLS)}
ac dec 60 .01 1G
let gr=real(v(od))
let gi=imag(v(od))
wrdata ac.dat gr gi
quit
.endc
.end
"""


def tran_deck(base, step, dt, dwell, device_traces=False):
    t0, t1, stop = 10, 10+dwell, 10+2*dwell
    vectors = NODE+(' '+MARGIN_COLUMNS if device_traces else '')
    return base+f"""EIP inp icm cmd od 0.5
EIM inn icm od cmd 0.5
VCMD cmd 0 PWL(0 {-step} {t0}u {-step} {t0+.01}u {step} {t1}u {step} {t1+.01}u {-step} {stop}u {-step})
.save {vectors}
{header()}tran {dt}n {stop}u 0 {dt}n
wrdata tran.dat {vectors}
quit
.endc
.end
"""


def load(path):
    array = np.loadtxt(path, skiprows=1, ndmin=2)
    if not np.isfinite(array).all():
        raise ValueError('Missing or nonfinite simulation data')
    return array


def calculate_op(job, meta):
    data = load(job/'op.dat')[0,1:]
    ac = load(job/'ac.dat')
    assert len(data)==6+len(COLS)
    f,real,imag = ac.T
    gain = 20*np.log10(np.abs(real+1j*imag))
    phase = np.unwrap(np.angle(real+1j*imag))*180/np.pi
    # Use the low-frequency sign as a confidence check on negative feedback.
    go = int(np.flatnonzero((gain[:-1]>=0)&(gain[1:]<0))[0]) if np.any((gain[:-1]>=0)&(gain[1:]<0)) else None
    frac = gain[go]/(gain[go]-gain[go+1]) if go is not None else np.nan
    ugf = float(f[go]*(f[go+1]/f[go])**frac) if go is not None else np.nan
    pm = float(180+phase[go]+frac*(phase[go+1]-phase[go])) if go is not None else np.nan
    result = dict(meta, gain_db=float(np.interp(.01,f,gain)), ugf_hz=ugf, phase_margin_deg=pm,
                  ac_low_freq_real=float(real[0]), out_cm_V=(data[2]+data[3])/2,
                  settled_out_diff_V=data[2]-data[3], bias_node_V=data[4],
                  vdd_current_uA=-data[5]*1e6, servo_input_diff_mV=(data[0]-data[1])*1e3)
    device_rows = []
    for i,(group,device) in enumerate((g,d) for g,ds in DEVICES.items() for d in ds):
        vd,vsat,idd,vg = data[6+4*i:10+4*i]
        device_rows.append(dict(meta, group=group, mos_instance=device, vds_V=vd, vdsat_V=vsat,
                                margin_mV=1e3*(abs(vd)-abs(vsat)), abs_id_uA=abs(idd)*1e6, vgs_V=vg))
    for group in DEVICES:
        ds = [x for x in device_rows if x['group']==group]
        result[group+'_min_margin_mV'] = min(x['margin_mV'] for x in ds)
        result[group+'_mean_current_uA'] = np.mean([x['abs_id_uA'] for x in ds])
    return result, device_rows


def settle_time(t, y, goal, threshold):
    worst = np.flatnonzero(np.any(np.abs(y-goal)>threshold, axis=1))
    if not len(worst):
        return float(t[0])
    i=worst[-1]+1
    return float(t[i]) if i<len(t) else np.nan


def calculate_tran(job, meta, step, dwell):
    a=load(job/'tran.dat')
    if a[-1,0] < (10+2*dwell-.01)*1e-6:
        raise ValueError('incomplete transient')
    durations=[]
    cm_errors=[]
    errors=[]
    for start,stop,direction in ((10,10+dwell,1),(10+dwell,10+2*dwell,-1)):
        t=a[:,0]*1e6
        edge=(t>=start)&(t<stop-.001)
        plateau=(t>=stop-4)&(t<=stop-1)
        ys=a[edge,1:3]
        final=np.mean(a[plateau,1:3],axis=0)
        target=np.array([2.5+direction*step/2,2.5-direction*step/2])
        measured=max(abs(final[0]-final[1]-direction*step),0)
        durations.append((settle_time(t[edge]-start,ys,final,.001*step),
                          settle_time(t[edge]-start,(ys[:,0]-ys[:,1])[:,None],
                                      direction*step,.001*2*step)))
        errors.append(measured*1e3)
        cm_errors.append(1e3*np.max(abs(np.mean(ys,axis=1)-2.5)))
    actual,target=map(list,zip(*durations))
    result = dict(meta, output_step_per_side_V=step, dwell_us=dwell,
                up_settle_us=actual[0],down_settle_us=actual[1],worst_settle_us=max(actual) if np.isfinite(actual).all() else np.nan,
                worst_target_diff_settle_us=max(target) if np.isfinite(target).all() else np.nan,
                worst_static_diff_error_mV=max(errors), peak_output_cm_error_mV=max(cm_errors))
    if a.shape[1] > 7:
        margin = (abs(a[:,7::2])-abs(a[:,8::2]))*1e3
        samples = a[:,0] >= 10e-6
        for group, ds in DEVICES.items():
            result[group+'_transient_min_margin_mV'] = float(np.min(margin[samples][:,[DEV.index(d) for d in ds]]))
    return result


def run(work, icm, iref, model, vdd, temp, rpp, mode, dt, step, dwell):
    job=work/f'{mode}_{model}_{vdd}_{temp}_{rpp}_cm{icm:.2f}_i{iref:g}_step{step:g}_dt{dt}'
    job.mkdir(exist_ok=True)
    meta=dict(input_cm_V=icm, iref_uA=iref, mos=model, supply_V=vdd, temperature_C=temp,
              rpp=rpp, case=job.name)
    base=fixture(icm,iref,model,vdd,temp,rpp)
    (job/'tb.cir').write_text(ac_deck(base) if mode=='ac' else tran_deck(base,step,dt,dwell,dt<=10))
    try:
        subprocess.run(['ngspice','-b','-o','run.log','tb.cir'], cwd=job,
                       capture_output=True, timeout=70, check=True)
        log=(job/'run.log').read_text()
        if re.search(r'(?im)^error|^fatal|simulation\(s\) aborted|timestep too small',log):
            raise ValueError('ngspice analysis stopped')
        result,devices=calculate_op(job,meta) if mode=='ac' else (calculate_tran(job,meta,step,dwell),[])
        result['status']='ok'
    except (OSError, ValueError, AssertionError, subprocess.SubprocessError) as e:
        result,devices=dict(meta,status=str(e)),[]
    print(job.name,result['status'],flush=True)
    return result,devices


def write(path, rows):
    if not rows:
        return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('work',type=Path)
    p.add_argument('--group',choices=('nominal','corners','fine','boundary','corner-boundary'),default='nominal')
    p.add_argument('--jobs',type=int,default=7)
    args=p.parse_args()
    args.work.mkdir(parents=True,exist_ok=True)
    nominal=('tntp',5,27,'typ')
    if args.group=='nominal':
        voltages=[round(i/100,2) for i in range(60,151,5)]+[.5,.55,1.6,1.8,2,2.2,2.5,2.7,2.8,2.9,3,3.1,3.2]
        cases=[(v,4.5,*nominal,'ac',20,0,0) for v in voltages]
        trans=[round(i/10,2) for i in range(6,16)]+[.85,.95,1.05,1.15,2.5]
        cases += [(v,4.5,*nominal,'tran',20,step,40) for v in trans for step in (.1,.25)]
        cases += [(v,3.5,*nominal,mode,20,.1 if mode=='tran' else 0,40) for v in (.6,.8,1,1.2,1.5) for mode in ('ac','tran')]
    elif args.group=='corners':
        conditions=[(m,5,27,'typ') for m in ('bnbp','bnwp','wnbp','wnwp')]
        conditions += [('bnwp',5.5,85,'worst'),('wnwp',4.5,0,'best')]
        cases=[(v,4.5,*c,mode,20,.1 if mode=='tran' else 0,40) for c in conditions
               for v in (.6,.8,1,1.2,1.5) for mode in ('ac','tran')]
    elif args.group=='fine':
        cases=[(v,4.5,*nominal,'tran',8,step,16) for v in (1.1,1.15,1.2,1.5) for step in (.1,.25)]
    elif args.group=='boundary':
        cases=[(v,4.5,*nominal,'ac',20,0,0) for v in (1.11,1.12,1.13,1.14,2.82,2.84,2.86,2.88,2.92,2.94,2.96,2.98)]
        cases += [(v,4.5,*nominal,'tran',50,step,220) for v in (.6,.65,.7) for step in (.1,.25)]
    else:
        weak=[('wnbp',5,27,'typ'),('wnwp',5,27,'typ'),('wnwp',4.5,0,'best'),('bnwp',5.5,85,'worst')]
        cases=[(v,4.5,*c,'ac',20,0,0) for c in weak for v in (1.25,1.3,1.35,1.4,1.45)]
        cases += [(v,4.5,*c,'tran',8,.25,40) for c in weak for v in (1.35,1.4,1.5)]
    with ThreadPoolExecutor(args.jobs) as pool:
        results=list(pool.map(lambda c:run(args.work,*c),cases))
    summary=[r for r,_ in results]
    write(args.work/f'{args.group}_ac.csv',[r for r in summary if r['case'].startswith('ac_')])
    write(args.work/f'{args.group}_transient.csv',[r for r in summary if r['case'].startswith('tran_')])
    write(args.work/f'{args.group}_devices.csv',[d for _,ds in results for d in ds])


if __name__=='__main__':
    main()
