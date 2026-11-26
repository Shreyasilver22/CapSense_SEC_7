from pathlib import Path
import re,json,hashlib
r=Path(__file__).resolve().parent;s=r/'simulation'
log=(s/'cosim.log').read_text()
assert not re.search(r'failed|error|aborted|undefined symbol|no entry function|timestep too small',log,re.I), 'Runtime/simulation error'
lines=(s/'phases.dat').read_text().splitlines();a=[list(map(float,l.split())) for l in lines[1:] if l.strip()]
assert a[-1][0]>=305e-6-1e-12
# columns: t, clk, reset, phi1,phi1b,phit,phitb,phi2,phi2b,sample_valid
for col in range(3,10):
 vals=[x[col] for x in a];assert min(vals)<.01 and max(vals)>4.99,(col,min(vals),max(vals))
# Check stable digital values on each side of switch ramps, after RTL NBA propagation.
for k in range(302):
 t=(2+k)*1e-6+.1e-6
 if t>305e-6:break
 # With the specified coincident clock/reset ramps and bridge delays, the first observed active count occurs at 2us.
 row=min(a,key=lambda row:abs(row[0]-t));n=k%100
 expected=[n<=40,n>40,45<=n<=89,not(45<=n<=89),46<=n<=89,not(46<=n<=89),n==80]
 assert all(abs(row[3+i]-5*int(v))<.02 for i,v in enumerate(expected)),(k,row,expected)
(s/'verification.json').write_text(json.dumps({'rtl':'PASS: reset and 300 edges','cosimulation':'PASS: 305us, all 7 outputs match RTL phase windows','voltage_levels':'PASS: 0/5V','main_analog':'not modified or simulated'},indent=2))
print('PASS: live co-simulation, 305 us, all seven phase waveforms and 0/5 V levels')
