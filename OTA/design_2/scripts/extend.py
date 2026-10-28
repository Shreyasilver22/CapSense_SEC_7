from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'scripts/analyze.py')};exec((R/'scripts/analyze.py').read_text().split('acs=[];trs=[]')[0],ns)
# The frozen snapshot already contains 6p/8p/10p variants.
vs=[]
for val in ['6p','8p','10p']:
 v=dict(name='metal_'+val+'_top_n2',value=val,orientation='top_n2');vs.append(v);text=ns['source'].replace('Cc n2 out {CC}','XCC n2 out vss scl08_cap_'+val);(R/'designs'/(v['name']+'.inc')).write_text(text)
acs=[];trs=[]
for v in vs:
 for cl in [1,5,10]:
  for vc in [1.5,2.5,3.5]:acs.append(ns['ac'](v,cl,vc))
 for cl in [1,5,10]:
  for large in [False,True]:trs.append(ns['trans'](v,cl,large))
 print('Extended',v['name'],flush=True)
for filename,rows in [('ac_checks.csv',acs),('settling_checks.csv',trs)]:
 with (R/'results'/filename).open() as f:old=[x for x in csv.DictReader(f) if x['name'] not in {v['name'] for v in vs}]
 with (R/'results'/filename).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(old+rows)
j=json.loads((R/'results/summary.json').read_text());j['nominal']=[x for x in j['nominal'] if x['name'] not in {v['name'] for v in vs}];j['ac_runs']=99;j['transient_runs']=66
for v in vs:
 a=next(x for x in acs if x['name']==v['name'] and x['CL_pF']==5 and x['VC_V']==2.5);s=next(x for x in trs if x['name']==v['name'] and x['CL_pF']==5 and not x['large_step']);l=next(x for x in trs if x['name']==v['name'] and x['CL_pF']==5 and x['large_step']);j['nominal'].append(dict(**a,small_worst_dynamic_us=s['worst_dynamic_us'],large_worst_dynamic_us=l['worst_dynamic_us'],small_static_error_mV=s['rise_static_error_mV'],minimum_checked_PM_deg=min(x['PM_deg'] for x in acs if x['name']==v['name'])))
valid=[x for x in j['nominal'] if x['name'].startswith('metal') and x['minimum_checked_PM_deg']>=60];j['selected']=min(valid,key=lambda x:x['large_worst_dynamic_us']) if valid else None
if j['selected']:
 j['selected_fine_large']=ns['trans']({k:j['selected'][k] for k in ['name','value','orientation']},5,True,1)
(R/'results/summary.json').write_text(json.dumps(j,indent=2));print(json.dumps(j['nominal'][-3:],indent=2))
