from pathlib import Path
import csv, hashlib, json, re, subprocess
import numpy as np

p=Path(__file__).parent
native=np.loadtxt(p/'results/symbol_export/symbol_ac.dat',skiprows=1)
hand=np.loadtxt(p/'results/equal_inputs/ac.dat',skiprows=1)
h=hand[:,1]+1j*hand[:,2]
h_native=-(native[:,1]+1j*native[:,2])
hi=np.interp(np.log10(native[:,0]),np.log10(hand[:,0]),h.real)+1j*np.interp(np.log10(native[:,0]),np.log10(hand[:,0]),h.imag)
assert np.allclose(h_native,hi,rtol=.002,atol=1e-7)
expected={
'M3 n1 n1 vdd vdd P w=2.5u l=3.2u m=1',
'M4 IOUT n1 vdd vdd P w=2.5u l=3.2u m=1',
'M1 n1 SP tail vss N w=2.5u l=3.2u m=1',
'M2 IOUT SENSE tail vss N w=2.5u l=3.2u m=1',
'M5 tail vbn vss vss N w=5u l=3.2u m=1'}
assert {x for x in (p/'designs/gm_ota.inc').read_text().splitlines() if x.startswith('M')}==expected
proof={'symbol_instance_pins':'sense sp vdd 0 vbn out',
       'native_vs_bench_max_relative_AC_difference':float(np.max(abs(h_native-hi)/np.maximum(abs(h_native),1e-20))),
       'source_files':{}}
for ext in ('sch','sym'):
 original=Path('/mnt/c/Users/HP/Downloads')/f'gm_ota.{ext}'
 copy=p/'designs'/original.name
 assert original.read_bytes()==copy.read_bytes()
 proof['source_files'][copy.name]=hashlib.sha256(copy.read_bytes()).hexdigest()
rows=[]
for step in (.1,2.):
 folder=p/'results'/f'follower_step_{step:g}'
 refine=p/'results'/f'follower_step_{step:g}_fine'
 refine.mkdir(exist_ok=True)
 b=(folder/'bench.cir').read_text().replace('tran 5n 90u 0 5n','tran 2n 90u 0 2n')
 (refine/'bench.cir').write_text(b)
 (refine/'.spiceinit').write_bytes((folder/'.spiceinit').read_bytes())
 subprocess.run(['ngspice','-b','-o','run.log','bench.cir'],cwd=refine,capture_output=True,check=True,timeout=80)
 a=np.loadtxt(folder/'transient.dat',skiprows=1)
 z=np.loadtxt(refine/'transient.dat',skiprows=1)
 for sample in (45e-6,85e-6):
  delta=float(np.interp(sample,a[:,0],a[:,2])-np.interp(sample,z[:,0],z[:,2]))
  assert abs(delta)<2e-6
  rows.append(dict(step_V=step,sample_us=sample*1e6,coarse_minus_fine_uV=delta*1e6))
proof['timestep_checks']=rows
(p/'results/verification.json').write_text(json.dumps(proof,indent=2))
print(json.dumps(proof,indent=2))
