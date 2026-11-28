"""Summarize the held output, acquisition sensitivity and track guard."""
from pathlib import Path
from collections import defaultdict
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_icm import ROOT, read_raw, measure
from waveform_checks import first_settled, window, write_table

HERE = Path(__file__).resolve().parent
SCL = ROOT / "schematic" / "netlist"
def prior_or_recorded(path, fallback):
    return path if path.is_file() else fallback


POINTS = [
    ("Flat baseline","typ",60,7.82,prior_or_recorded(ROOT/"runs/int_flat60_low/trace.raw",ROOT/"runs/low_current_low/trace.raw")),
    ("Flat baseline","typ",60,11.79,prior_or_recorded(ROOT/"runs/int_flat60_high/trace.raw",ROOT/"runs/low_current_high/trace.raw")),
    ("Xschem baseline","typ",60,7.82,HERE/"runs/int_xschem60_low/trace.raw"),
    ("Xschem baseline","typ",60,11.79,prior_or_recorded(HERE/"runs/int_xschem60_high/trace.raw",SCL/"xschem.raw")),
]
for tag,cp in (("low",7.82),("high",11.79)):
    for bank in (48,40):
        POINTS.append((f"Flat {bank} units","typ",bank,cp,ROOT/f"runs/int_flat{bank}_{tag}/trace.raw"))
    POINTS.append(("Xschem 40 units","typ",40,cp,HERE/f"runs/int_xschem40_{tag}/trace.raw"))
    for corner in ("cold","hot"):
        POINTS.append((f"Flat 40 {corner}",corner,40,cp,ROOT/f"runs/int_{corner}40_{tag}/trace.raw"))


def crossing(t, v, threshold, rising):
    indices = np.flatnonzero((v[:-1]<threshold)&(v[1:]>=threshold) if rising
                             else (v[:-1]>=threshold)&(v[1:]<threshold))
    if len(indices)!=1:
        raise ValueError(f"Expected one {threshold:g} V crossing, found {len(indices)}")
    i = indices[0]
    return t[i]+(t[i+1]-t[i])*(threshold-v[i])/(v[i+1]-v[i])


def metrics(path,corner):
    wave = read_raw(path)
    stop = wave["time"][-1]*1e6
    delay = 100 if corner=='cold' else 0
    rail = {'typ':5,'cold':4.5,'hot':5.5}[corner]
    cycles = round((stop+5-delay)/100)
    if abs(stop - (cycles*100-5+delay)) > .01 or cycles < 10:
        raise ValueError(f"Incomplete transient {path} ({stop:.3f} µs)")
    rows = measure(wave,delay,cycles,rail)
    cm_cycle = delay+(cycles-1)*100
    open_t,close_t=window(wave,cm_cycle,rail)
    time = wave["time"]*1e6-cm_cycle
    interp = lambda sig, t: np.interp(t,time,wave[sig])
    win = (time >= open_t) & (time <= close_t)
    in_cm = (wave["v(sump)"]+wave["v(sumn)"])/2
    guard_win = (time>=76)&(time<=90)
    t_close = crossing(time[guard_win],wave["v(tr)"][guard_win],rail/2,False)
    adc_start = crossing(time[guard_win],wave["v(adc_sw)"][guard_win],.5,True)
    late = interp("v(outp)",t_close-.3)-interp("v(outn)",t_close-.3)
    held = interp("v(pinp)",adc_start-.05)-interp("v(pinn)",adc_start-.05)
    sample_cm = (interp("v(outp)",85)+interp("v(outn)",85))/2
    return (dict(**rows[-1], settled_cycle=first_settled(rows),
                 sample_cm_error_max_mV=1e3*np.max(np.abs(in_cm[win]-2.5)),
                 track_close_us=t_close, adc_edge_us=adc_start,
                 adc_guard_ns=(adc_start-t_close)*1000, hold_vs_live_mV=(held-late)*1000,
                 output_sample_cm_V=sample_cm), rows)


def make_plot(points, pairs):
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig, axes=plt.subplots(1,2,figsize=(11.7,4.4))
    colors={"Flat baseline":"#236583","Xschem baseline":"#687c8e",
            "Flat 48 units":"#328366","Flat 40 units":"#bb652d","Xschem 40 units":"#77558b"}
    for name,g in pairs.items():
        if name not in colors:
            continue
        color=colors[name]
        axes[0].plot([row["cp_pF"] for row in g],[row["held_at_88_mV"] for row in g],
                     marker="o",label=name,color=color)
    axes[0].grid(alpha=.25)
    axes[0].set(xlabel="CP (pF), CN = 10 pF",ylabel="Held differential output (mV)")
    axes[0].legend(frameon=False)
    points = [r for r in points if r['corner']=='typ']
    x=np.arange(len(points))
    axes[1].bar(x-.17,[r["held_sensitivity_mV_pF"] for r in points],.34,label="Held output",color="#236583")
    axes[1].bar(x+.17,[r["adc_sensitivity_mV_pF"] for r in points],.34,label="Modeled ADC input",color="#9abfcd")
    axes[1].set(xticks=x,xticklabels=["Flat\n60 units","Xschem\n60 units","Flat\n48 units","Flat\n40 units","Xschem\n40 units"],
                ylabel="Endpoint sensitivity (mV/pF)")
    axes[1].set_ylim(0,1.28*max(r["held_sensitivity_mV_pF"] for r in points))
    axes[1].legend(frameon=False,loc="upper left",ncols=2)
    fig.suptitle("Integrated SC + OTA sensitivity with the SCL08 input-CM controller",fontweight="bold")
    fig.tight_layout()
    fig.savefig(HERE/"Integrated_Sensitivity.png",dpi=185)


def main():
    rows=[]
    pairs=defaultdict(list)
    for label,corner,fb,cp,path in POINTS:
        result,_=metrics(path,corner)
        row=dict(method=label,corner=corner,cp_pF=cp,cn_pF=10,fb_per_branch=fb,**result)
        rows.append(row)
        pairs[label].append(row)
    slopes=[]
    for label,(lo,hi) in pairs.items():
        dc=hi["cp_pF"]-lo["cp_pF"]
        dv=lambda key:(hi[key]-lo[key])/dc
        slopes.append(dict(method=label,corner=hi['corner'],fb_per_branch=hi["fb_per_branch"],
                           held_sensitivity_mV_pF=dv("held_at_88_mV"),
                           adc_sensitivity_mV_pF=dv("adc_at_89_mV"),
                           late_live_sensitivity_mV_pF=dv("live_at_85_mV"),
                           worst_cm_error_mV=max(lo["sample_cm_error_max_mV"],hi["sample_cm_error_max_mV"]),
                           min_adc_guard_ns=min(lo["adc_guard_ns"],hi["adc_guard_ns"]),
                           max_abs_hold_delta_mV=max(abs(lo["hold_vs_live_mV"]),abs(hi["hold_vs_live_mV"])),
                           max_startup_cycles=max(lo["settled_cycle"] or float("inf"),hi["settled_cycle"] or float("inf")),
                           vdd_mW_hi=hi["vdd_mW"]))
    write_table(HERE/"integrated_points.csv",rows)
    write_table(HERE/"integrated_sensitivity.csv",slopes)
    make_plot(slopes,pairs)
    for row in slopes:
        print(row)

if __name__=="__main__":
    main()
