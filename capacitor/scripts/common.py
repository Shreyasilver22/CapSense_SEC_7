from pathlib import Path
import re,math,json
ROOT=Path(__file__).resolve().parents[1]
def parse_value(value):
 m=re.fullmatch(r'([+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)([fpnum]?)',value,re.I)
 if not m:raise ValueError('Use a positive concrete SPICE value, e.g. 2.5p, 7.5p, 3p or 11.384f; expressions are not layout requests: '+value)
 number=float(m[1])*{'':1,'f':1e-15,'p':1e-12,'n':1e-9,'u':1e-6,'m':1e-3}[m[2].lower()]
 if not math.isfinite(number) or number<=0:raise ValueError('Capacitance must be positive and finite')
 return number
def requests():
 j=json.loads((ROOT/'requests.json').read_text());items=[];seen=set()
 for spec in j['capacitors']:
  value=spec['value'];target=parse_value(value)
  if value.lower() in seen:raise ValueError('Duplicate value token: '+value)
  seen.add(value.lower());n=spec.get('units',int(target/(j['unit_C_fF']*1e-15)+.5))
  if not isinstance(n,int) or not 1<=n<=4096:raise ValueError('Requested value requires between 1 and 4096 units; no silent clipping: '+value)
  cols=max(1,math.ceil(math.sqrt(n*28/40)));rows=math.ceil(n/cols)
  items.append({**spec, 'target_F':target,'units':n,'columns':cols,'rows':rows,'cell':'scl08_cap_n%d'%n})
 return items
