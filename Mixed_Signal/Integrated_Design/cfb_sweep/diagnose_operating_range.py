from pathlib import Path
import subprocess,concurrent.futures,json,numpy as np
R=Path(__file__).resolve().parent
names=['outp','outn','sump','sumn','sample_valid','phi1','phit','phi2','txp','txn','rxp','rxn','sensp','sensn']
def run(tag):
 source=R/'runs_replay'/tag;row=json.loads((source/'result.json').read_text());d=R/'operating_range_diagnostics'/tag;d.mkdir(parents=True,exist_ok=True)
 s=(source/'bench.cir').read_text();s=s.replace('save v(outp) v(outn) v(sump) v(sumn) v(sample_valid) v(phi1) v(phit) v(phi2)','save '+' '.join('v('+n+')' for n in names));s=s.replace('wrdata tail.dat v(outp) v(outn) v(sump) v(sumn) v(sample_valid) v(phi1) v(phit) v(phi2)','wrdata diagnostic.dat '+' '.join('v('+n+')' for n in names));(d/'bench.cir').write_text(s);(d/'.spiceinit').write_text((R.parent/'simulation/.spiceinit').read_text())
 with (d/'launcher.log').open('w') as f:subprocess.run(['nice','-n','10','ngspice','-b','-o','diagnostic.log','bench.cir'],cwd=d,stdout=f,stderr=f,timeout=300)
 a=np.loadtxt(d/'diagnostic.dat',skiprows=1);end=row['cycles']*100-100
 result={'case':tag,'ranges':{n:[float(a[:,i+1].min()),float(a[:,i+1].max())] for i,n in enumerate(names)},'phases':{str(t):{n:float(np.interp((end+t)*1e-6,a[:,0],a[:,i+1])) for i,n in enumerate(names)} for t in [10,40,47.5,48.5,50,70,83]}}
 (d/'diagnostic.json').write_text(json.dumps(result,indent=2));return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,['cfb40_cp1_cn1p5','cfb40_cp1_cn12']))
(R/'operating_range_diagnostics.json').write_text(json.dumps(rows,indent=2))
