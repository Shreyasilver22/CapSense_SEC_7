#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,re
r=Path(__file__).resolve().parent;s=r/'simulation';runtime=Path('/home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench')
for name,target in [('capsense_phase_runtime',runtime),('capsense_integrated',r)]:
 p=Path('/tmp')/name
 if p.is_symlink():
  if p.resolve()!=target:sys.exit('Unexpected alias target: '+str(p))
 elif p.exists():sys.exit('Alias path occupied: '+str(p))
 else:p.symlink_to(target,target_is_directory=True)
subprocess.run([str(runtime/'runtime/bin/iverilog'),'-s','capsense_phase_gen','-o',str(s/'capsense_phase_gen.vvp'),str(r/'rtl/capsense_phase_gen.v')],check=True)
subprocess.run(['xschem-800nm','-x','-q','--tcl','set USER_CONF_DIR /tmp','-s','-n','-o',str(s),str(r/'schematic/capsense_integrated_tb.sch')],check=True,cwd=r)
p=subprocess.run(['ngspice','-b','-o','integrated_run.log','capsense_integrated_tb.spice'],cwd=s,timeout=900)
log=(s/'integrated_run.log').read_text()
if re.search(r'error|aborted|timestep too small|failed|no entry function',log,re.I):sys.exit('Simulation failed; inspect simulation/integrated_run.log')
f=(s/'exp1_clocks.dat').open();next(f);a=[list(map(float,l.split())) for l in f]
assert a[-1][0]>=795e-6-1e-12
for col in range(1,8):assert min(x[col] for x in a)<.1 and max(x[col] for x in a)>4.9
print('PASS: 795 us transient and all seven phase outputs. Analog accuracy requires review.')
