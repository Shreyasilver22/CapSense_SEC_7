#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,os
r=Path(__file__).resolve().parent;s=r/'simulation';iv=r/'runtime/bin/iverilog';vv=r/'runtime/bin/vvp'
os.environ['LD_LIBRARY_PATH']=str(r/'runtime/lib')+':'+os.environ.get('LD_LIBRARY_PATH','')
if not iv.is_file() or not vv.is_file():sys.exit('Private runtime not built yet: see simulation/build_iverilog_resume.log')
for cmd in [[str(iv),'-s','rtl_testbench','-o','rtl_testbench.vvp','rtl_testbench.v','../rtl/capsense_phase_gen.v'],[str(vv),'rtl_testbench.vvp'],[str(iv),'-s','capsense_phase_gen','-o','capsense_phase_gen.vvp','../rtl/capsense_phase_gen.v'],['xschem','-x','-q','--rcfile',str(r/'xschemrc'),'-s','-n','-o',str(s),str(r/'schematic/phase_generator_tb.sch')]]:
 subprocess.run(cmd,cwd=s,check=True)
subprocess.run(['ngspice','-b','-o','cosim.log','phase_generator_tb.spice'],cwd=s,timeout=60)
subprocess.run([sys.executable,str(r/'validate_cosim.py')],cwd=s,check=True)
