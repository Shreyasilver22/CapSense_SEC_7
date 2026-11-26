from pathlib import Path
import os,subprocess
os.environ['CAPSENSE_RTL_REPLAY']='1'
import sweep
R=sweep.R;d=R/'timeout_debug';d.mkdir(exist_ok=True)
s=sweep.deck(40,1.,4.,8,80)
s=s.replace('tran 80n 795u 600u 80n','''stop when time = 1u
stop when time = 10u
stop when time = 50u
stop when time = 85u
stop when time = 100u
stop when time = 200u
stop when time = 400u
tran 80n 795u 0 80n
echo AT_1U
print time[length(time)-1]
resume
echo AT_10U
print time[length(time)-1]
resume
echo AT_50U
print time[length(time)-1]
resume
echo AT_85U
print time[length(time)-1]
resume
echo AT_100U
print time[length(time)-1]
resume
echo AT_200U
print time[length(time)-1]
resume
echo AT_400U
print time[length(time)-1]
resume''')
(d/'bench.cir').write_text(s);(d/'.spiceinit').write_text((sweep.P/'simulation/.spiceinit').read_text())
try:subprocess.run(['ngspice','-b','-o','debug.log','bench.cir'],cwd=d,timeout=120)
except subprocess.TimeoutExpired:print('Timed out; inspect last checkpoint')
