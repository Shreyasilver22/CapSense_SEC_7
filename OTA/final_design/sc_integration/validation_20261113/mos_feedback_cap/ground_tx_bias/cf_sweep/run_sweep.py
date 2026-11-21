"""Sweep feedback bank size with TX at ground and IREF at 4.5 µA."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from sweep import build, PROBES, run_spice, write_csv

COUNTS = (48,73,97,121,145,194,291,388)
CASES = ((12,7),(12,12),(11.95,7),(12.05,7))


def run(folder, count, cp, cn, *, step="30n", perturb=None):
    body = build(4.5,cp,cn,"tntp49_5v",5,27).replace("M=97 AD=",f"M={count} AD=")
    if perturb is not None:
        b,sign=perturb
        cap=cp if b=="p" else cn
        body += f"IPERT tx{b} rx{b} PULSE(0 {sign*cap*1e-7} 143u 1n 1n 9n 1m)\n"
    probes=" ".join(PROBES)
    commands=(f"set klu\nsave all {probes}\ntran {step} 200u 0 {step}\n"
              f"wrdata wave.dat v(outp) v(outn) v(sump) v(sumn) v(rxp) v(rxn) {probes}")
    wave=run_spice(folder,"cf_sweep",body,commands,"wave.dat")
    if wave[-1,0] < 199.99e-6:
        raise RuntimeError(f"Incomplete transient in {folder}")
    t,op,on,ip,inn,rp,rn,*junction=wave.T
    time=t*1e6-100
    d=op-on
    sample=lambda v,at=80:float(np.interp(at,time,v))
    if perturb is not None:
        return sample(d)
    cycle=time>=0
    edge=(time>=45)&(time<=55)
    icm,ocm=(ip+inn)/2,(op+on)/2
    late=sample(d,88)
    outside=np.flatnonzero((time>=46)&(time<=88)&(abs(d-late)>max(abs(late)*.001,100e-6)))
    if cp==cn and step=="30n":
        np.savetxt(OUT/f"balanced_wave_{count}.csv",
                   np.column_stack((time[cycle],icm[cycle],ocm[cycle],rp[cycle],rn[cycle])),
                   delimiter=",",header="time_us,input_cm_v,output_cm_v,rxp_v,rxn_v",comments="")
    return dict(units=count,cp_pf=cp,cn_pf=cn,step=step,diff_mv=1e3*sample(d),
                sampled_out_cm_v=sample(ocm), min_in_cm_v=min(icm[cycle]),
                min_out_cm_v=min(ocm[cycle]), min_rx_v=min(min(rp[cycle]),min(rn[cycle])),
                max_rx_junction_ua=1e6*np.max(np.abs(junction)[:,edge]),
                rx_junction_abs_charge_fc=1e9*np.trapz(np.abs(junction)[:,edge].sum(axis=0),time[edge]),
                settle_us=time[outside[-1]+1]-46 if len(outside) else 0,
                late_change_uv=1e6*(late-sample(d)))


def main():
    unit_pf=float(np.interp(-.5,*np.genfromtxt(OUT.parents[1]/"pmos_cv.csv",delimiter=",",skip_header=1).T))*1e12
    with TemporaryDirectory(prefix="sc-ground-cf-") as tmp, ThreadPoolExecutor(max_workers=6) as pool:
        work=Path(tmp)
        nominal={(m,p,n):pool.submit(run,work/f"nom_{m}_{p}_{n}",m,p,n) for m in COUNTS for p,n in CASES}
        noise={(m,b,s):pool.submit(run,work/f"noise_{m}_{b}_{s}",m,12,7,perturb=(b,s))
               for m in COUNTS for b in "pn" for s in (-1,1)}
        fine=[pool.submit(run,work/f"fine_{m}_{n}",m,12,n,step="10n") for m in (97,194,291,388) for n in (7,12)]
        rows={k:job.result() for k,job in nominal.items()}
        write_csv(OUT/"transients.csv",list(rows.values()))
        summary=[]
        for m in COUNTS:
            signal,balanced=rows[m,12,7],rows[m,12,12]
            slope=(rows[m,12.05,7]["diff_mv"]-rows[m,11.95,7]["diff_mv"])/.1
            variance=sum(1.380649e-23*300.15/(cap*1e-12)*
                         ((noise[m,b,1].result()-noise[m,b,-1].result())/.002)**2
                         for b,cap in (("p",12),("n",7)))
            rms=np.sqrt(variance)*1e6
            summary.append(dict(nominal_cf_pf=m*unit_pf,units=m,diff_mv=signal["diff_mv"],
                                sensitivity_mv_pf=slope,sensor_noise_uv=rms,
                                sensor_noise_af=1000*rms/abs(slope),settle_us=signal["settle_us"],
                                balanced_min_rx_v=balanced["min_rx_v"],
                                balanced_min_in_cm_v=balanced["min_in_cm_v"],
                                balanced_min_out_cm_v=balanced["min_out_cm_v"],
                                balanced_junction_charge_fc=balanced["rx_junction_abs_charge_fc"]))
        write_csv(OUT/"summary.csv",summary)
        write_csv(OUT/"fine.csv",[j.result() for j in fine])


if __name__=="__main__":
    main()
