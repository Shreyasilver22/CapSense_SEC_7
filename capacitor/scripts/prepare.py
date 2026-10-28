"""Resolve editable symbol values into checked models/layouts. No ideal-cap fallback."""
from pathlib import Path
import argparse,json,re,subprocess,sys
from common import ROOT as R,parse_value
p=argparse.ArgumentParser();p.add_argument('--schematic',type=Path);p.add_argument('--value',action='append',default=[]);p.add_argument('--pdk-root',required=True);a=p.parse_args();values=list(a.value)
if a.schematic:
 s=a.schematic.read_text()
 for m in re.finditer(r'C\s+\{[^}]*scl08_cap[23]\.sym\}[^\n]*\{([^{}]*)\}',s):
  v=re.search(r'(?:^|\s)value=("[^"]*"|[^\s]+)',m[1])
  if not v:raise SystemExit('Capacitor instance missing value')
  values.append(v[1].strip('"'))
if not values:raise SystemExit('No values found. Pass --value 4p or --schematic file.sch (top-level capacitor instances).')
j=json.loads((R/'requests.json').read_text());known={x['value'].lower() for x in j['capacitors']}
for value in values:
 parse_value(value)
 if value.lower() not in known:j['capacitors'].append({'value':value,'note':'Requested through prepare.py; nearest integer unit count'});known.add(value.lower())
(R/'requests.json').write_text(json.dumps(j,indent=2)+'\n')
subprocess.run([sys.executable,str(R/'scripts/build.py'),'--pdk-root',a.pdk_root],check=True)
print('Prepared values:',', '.join(values));print('Reload models/catalog.tcl or restart xschem to refresh extracted-value labels. Layouts/models/catalog have been regenerated.')
