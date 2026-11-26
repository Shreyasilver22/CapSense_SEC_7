from pathlib import Path
import json
R=Path(__file__).resolve().parent
source=Path('/home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench/simulation/phases.dat')
f=source.open();next(f);a=[list(map(float,l.split())) for l in f]
cols={'phi1':3,'phi1b':4,'phit':5,'phitb':6,'phi2':7,'phi2b':8,'sample_valid':9}
result={}
for name,c in cols.items():
 events=[]
 for x,y in zip(a,a[1:]):
  if (x[c]>2.5)!=(y[c]>2.5):
   cross=x[0]+(2.5-x[c])*(y[0]-x[0])/(y[c]-x[c]);events.append([cross-.5e-9,5. if y[c]>2.5 else 0.])
 result[name]={'initial':0.,'initial_events':[e for e in events if e[0]<100e-6],'periodic_events':[[e[0]-100e-6,e[1]] for e in events if 100e-6<=e[0]<200e-6]}
(R/'rtl_recorded_edges.json').write_text(json.dumps({'source':str(source),'recorded_DAC_slew_s':1e-9,'sweep_DAC_slew_s':1e-6,'period_s':100e-6,'signals':result},indent=2))
