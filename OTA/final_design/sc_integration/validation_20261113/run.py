"""Reproduce the nominal SC sensitivity, common-mode, and held-phase noise checks."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import csv
import math
import re
import subprocess
import tempfile

import numpy as np

OUTPUT = Path(__file__).resolve().parent
DESIGN = Path.home() / "final year project/ota/final_design"
BENCH = DESIGN / "sc_integration/tb/sc_cmfb.cir"
SAMPLE_US = 480
SIGNALS = ["outp", "outn", "sump", "sumn", "phi1", "phi2", "phit", "txp", "rxp", "txn", "rxn"]
BANDS = (5000, 10000, 10000000)

def run_spice(folder, title, body, commands, filename):
    folder.mkdir(parents=True)
    deck = folder / f"{title}.cir"
    deck.write_text(body + "\n.control\nset wr_singlescale\nset wr_vecnames\nset numdgt=15\n"
                    + commands + "\nquit\n.endc\n.end\n")
    log = subprocess.run(["ngspice", "-b", deck.name], cwd=folder, check=True,
                         capture_output=True, text=True)
    (folder / "ngspice.log").write_text(log.stdout + log.stderr)
    data = np.loadtxt(folder / filename, skiprows=1)
    if not np.isfinite(data).all():
        raise ValueError(f"Non-finite result in {folder}")
    return data

def circuit(cp, cn):
    deck = BENCH.read_text().split(".control")[0]
    deck = deck.replace('"../../models/', f'"{DESIGN}/models/')
    return deck.replace(".param CP=7p CN=5p CF=40p", f".param CP={cp}p CN={cn}p CF=40p")

def transient(folder, cp, cn, step="20n"):
    commands = f"tran {step} 500u 0 {step}\nwrdata wave.dat " + " ".join(f"v({n})" for n in SIGNALS)
    wave = run_spice(folder, "transient", circuit(cp, cn), commands, "wave.dat")
    assert wave[-1, 0] >= 499.99e-6, folder
    return wave

def metrics(wave, cp, cn):
    time = wave[:, 0] * 1e6
    op, on, ip, inn = wave[:, 1:5].T
    diff, out_cm, in_cm = op - on, (op + on) / 2, (ip + inn) / 2
    sample = lambda values, at=SAMPLE_US: np.interp(at, time, values)
    cycle = (time >= 400) & (time < 500)
    return dict(cp_pf=cp, cn_pf=cn, delta_pf=cp-cn, total_pf=cp+cn,
                sample_us=SAMPLE_US, out_diff_v=sample(diff),
                ideal_diff_v=15*(cp-cn)/(80+cp+cn),
                out_cm_v=sample(out_cm), in_cm_v=sample(in_cm),
                ideal_in_cm_v=(200-5*(cp+cn))/(80+cp+cn),
                reset_in_cm_v=sample(in_cm,430), reset_out_cm_v=sample(out_cm,430),
                in_cm_min_v=min(in_cm[cycle]), in_cm_max_v=max(in_cm[cycle]),
                out_cm_min_v=min(out_cm[cycle]), out_cm_max_v=max(out_cm[cycle]))

def held_noise(folder, cp, cn, wave):
    sample = [np.interp(SAMPLE_US*1e-6, wave[:,0], wave[:,i]) for i in range(1,12)]
    deck = circuit(cp, cn)
    for clock, level in [("VPHI1", 0), ("VPHI2", 5), ("VPHIT", 5)]:
        deck = re.sub(rf"^{clock} (\w+) 0 PULSE.*$", rf"{clock} \1 0 DC {level}",
                      deck, flags=re.M)
    deck = deck.replace("VREF vref 0 2.5", "VREF vref 0 DC 2.5 AC 1")
    # Reproduce the sampled DC bias. The inductors are effectively open
    # throughout the AC/noise band. All transmission gates remain in the deck.
    for index, (node, bias) in enumerate(zip(SIGNALS, sample)):
        if node.startswith("phi"):
            continue
        deck += f"V_HOLD{index} hold{index} 0 {bias:.15g}\nL_HOLD{index} hold{index} {node} 1e12\n"
    deck += "ECMP ocm mid outp 0 0.5\nECMN mid 0 outn 0 0.5\n"
    deck += "EIMP icm imid sump 0 0.5\nEIMN imid 0 sumn 0 0.5\n"
    results = {}
    for label, output in [("differential","v(outp,outn)"), ("output_cm","v(ocm)"),
                          ("input_cm","v(icm)")]:
        commands = f"noise {output} VREF dec 50 1 10Meg\nsetplot noise1\nwrdata noise.dat onoise_spectrum"
        data = run_spice(folder / label, "held", deck, commands, "noise.dat")
        assert data[0,0] == 1 and data[-1,0] >= 9.999e6 and max(data[:,1]) > 0
        results[label] = data
    return results

def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    differential = [(6+d/2, 6-d/2) for d in np.linspace(-2,2,9)]
    totals = [(c,c) for c in [5,5.5,6.5,7]] + [(6.975,5.025), (7.025,4.975)]
    cases = differential + totals
    with tempfile.TemporaryDirectory(prefix="sc-ota-") as temp:
        work = Path(temp)
        def run_case(pair):
            cp, cn = pair
            return transient(work/f"cp{cp}_cn{cn}", cp, cn)
        with ThreadPoolExecutor(max_workers=4) as pool:
            waves = dict(zip(cases,pool.map(run_case,cases)))
            fine = pool.submit(transient, work/"fine", 7, 5, "5n")
            jobs = {pair: pool.submit(held_noise, work/f"noise{pair[0]}", *pair, waves[pair])
                    for pair in [(6,6),(7,5)]}
            rows = [metrics(waves[pair], *pair) for pair in cases]
            write_csv(OUTPUT/"sampled_results.csv", rows)
            write_csv(OUTPUT/"timestep_check.csv",[metrics(fine.result(),7,5)])
            wave = waves[7,5]
            np.savetxt(OUTPUT/"nominal_last_cycle.csv", wave[wave[:,0]>=400e-6],
                       delimiter=",", header="time_s," + ",".join(SIGNALS), comments="")
            noise_rows = []
            for pair, future in jobs.items():
                data = future.result()
                freq = data["differential"][:,0]
                for label, spectrum in data.items():
                    for band in BANDS:
                        below = freq < band
                        x = np.r_[freq[below],band]
                        asd = np.r_[spectrum[below,1],np.interp(band,freq,spectrum[:,1])]
                        rms = math.sqrt(np.trapz(asd**2,x))
                        noise_rows.append(dict(cp_pf=pair[0],cn_pf=pair[1],mode=label,
                                               band_low_hz=1, band_high_hz=band,rms_v=rms))
                np.savetxt(OUTPUT/f"noise_cp{pair[0]}_cn{pair[1]}.csv",
                           np.column_stack([freq, *[v[:,1] for v in data.values()]]), delimiter=",",
                           header="frequency_hz,differential_v_per_sqrt_hz,output_cm_v_per_sqrt_hz,input_cm_v_per_sqrt_hz",
                           comments="")
            write_csv(OUTPUT/"noise_summary.csv", noise_rows)
            for pair in jobs:
                for label in ("differential","output_cm","input_cm"):
                    log = work/f"noise{pair[0]}"/label/"ngspice.log"
                    (OUTPUT/f"noise_cp{pair[0]}_cn{pair[1]}_{label}.log").write_text(log.read_text())
    slope, intercept = np.polyfit([r["delta_pf"] for r in rows[:9]], [r["out_diff_v"] for r in rows[:9]],1)
    residual = max(abs(r["out_diff_v"]-(slope*r["delta_pf"]+intercept)) for r in rows[:9])
    print(f"Fixed-total slope {slope:.9g} V/pF; intercept {intercept:.9g} V; peak residual {residual:.9g} V")
    print(rows[8])

if __name__ == "__main__":
    main()
