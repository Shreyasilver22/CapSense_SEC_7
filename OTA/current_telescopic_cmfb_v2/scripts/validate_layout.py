import json,itertools,concurrent.futures,sys
import sweep as w,sc_simulate as s
R=w.R
if __name__=='__main__':
 p=json.loads((R/'selected.json').read_text());model=R/'models/layout_C.spice'
 configs=[dict(mos=m,vdd=v,temp=t,res=r) for m,v,t,r in itertools.product(['tntp49_5v','bnbp49_5v','bnwp49_5v','wnbp49_5v','wnwp49_5v'],[4.5,5,5.5],[0,27,85],['best','typ','worst'])]
 jobs=[]
 for c in configs:
  for kind in ['cm','diff']:
   for vd,cl in [(0,1),(0,10),(6.6-c['vdd'],10),(-(6.6-c['vdd']),10)]:jobs.append(dict(**c,kind=kind,vd=vd,cl=cl))
 # Nominal, CL=5 pF, both modes.
 jobs += [dict(kind=k,cl=5) for k in ['cm','diff']]
 if '--sc-only' not in sys.argv:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(lambda j:w.ac(p,model=model,tag='extracted',**j),jobs))
  w.save('extracted_ac',rows)
  for kind in ['cm','diff']:
   a=[x for x in rows if x['kind']==kind and x['status']=='OK' and x['PM_deg'] is not None]
   print(kind,'cases',len(a),'minPM',min(a,key=lambda x:x['PM_deg']),flush=True)
 jobs=[dict(arch=a,switch=sw) for a,sw in itertools.product(['schematic','layout_C'],['smooth','tg'])]
 jobs += [dict(arch='layout_C',switch=sw,fs=f) for sw,f in itertools.product(['smooth','tg'],[100000,200000])]
 jobs += [dict(arch='layout_C',switch=sw,mos=m,vdd=v,temp=t) for sw,(m,v,t) in itertools.product(['smooth','tg'],[('wnwp49_5v',4.5,85),('bnbp49_5v',5.5,0)])]
 jobs += [dict(arch='layout_C',switch=sw,dt=2) for sw in ['smooth','tg']]
 jobs += [dict(arch='layout_C',switch='tg',dt=2,delta=.05),dict(arch='layout_C',switch='tg',load=10)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rr=list(ex.map(lambda j:s.run(method='gear',**j),jobs))
 s.save('SC_validation',rr);print('SC cases',len(rr),flush=True)
