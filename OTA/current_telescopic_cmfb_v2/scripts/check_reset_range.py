import json,itertools,concurrent.futures
import sweep as w
if __name__=='__main__':
 p=json.loads((w.R/'selected.json').read_text());jobs=[]
 for m,v,t,r,k,sign in itertools.product(['tntp49_5v','bnbp49_5v','bnwp49_5v','wnbp49_5v','wnwp49_5v'],[5,5.5],[0,27,85],['best','typ','worst'],['cm','diff'],[-1,1]):
  jobs.append(dict(mos=m,vdd=v,temp=t,res=r,kind=k,vd=sign*(v-3),cl=10))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(lambda j:w.ac(p,model=w.R/'models/layout_C.spice',tag='extracted',**j),jobs))
 w.save('reset_range_ac',rows)
 for k in ['cm','diff']:
  rr=[x for x in rows if x['status']=='OK' and x['kind']==k and x['PM_deg'] is not None];print(k,'minPM',min(rr,key=lambda x:x['PM_deg']),flush=True)
