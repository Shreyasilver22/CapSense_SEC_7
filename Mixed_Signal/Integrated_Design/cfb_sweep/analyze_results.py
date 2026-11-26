from pathlib import Path
import sys,os,json,math
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'plotting_deps'));os.environ['MPLCONFIGDIR']=str(R/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'figure.dpi':150,'savefig.bbox':'tight','savefig.pad_inches':0.12})
O=Path(os.environ.get('CAPSENSE_ANALYSIS_OUTPUT',str(R)));O.mkdir(parents=True,exist_ok=True)
LABEL=os.environ.get('CAPSENSE_PLOT_LABEL','')
rows=json.loads(Path(os.environ.get('CAPSENSE_RESULTS_FILE',str(R/'sweep_results_replay.json'))).read_text());assert len(rows)==1587
by={(r['cfb_nominal_pF'],r['cp_pF'],r['cn_pF']):r for r in rows};assert len(by)==1587
x=np.arange(1,12.01,.5);fields=['vdiff_V','input_vcm_V','output_vcm_V','voutp_V','voutn_V'];summary={};grid={}
for cf in [40,50,60]:
 sub=[by[(cf,float(cp),float(cn))] for cp in x for cn in x]
 valid=np.array([r['complete'] and r['settled'] for r in sub]).reshape(23,23)
 arrays={key:np.array([r.get(key,np.nan) if r['complete'] else np.nan for r in sub]).reshape(23,23) for key in fields}
 y=np.where(valid,arrays['vdiff_V'],np.nan)
 dp=np.gradient(y,.5,axis=0,edge_order=2);dn=np.gradient(y,.5,axis=1,edge_order=2);diff=.5*(dp-dn)
 arrays.update(sensitivity_cp_mV_per_pF=dp*1000,sensitivity_cn_mV_per_pF=dn*1000,sensitivity_delta_mV_per_pF=diff*1000,valid=valid)
 for i,cp in enumerate(x):
  for j,cn in enumerate(x):
   row=by[(cf,float(cp),float(cn))]
   if row['complete']:
    row['vdiff_cycle_change_mV']=abs(row['vdiff_V']-row['previous_vdiff_V'])*1000
    row['cfb_gate_bias_p_approx_V']=row['voutp_V']-row['input_vcm_V']
    row['cfb_gate_bias_n_approx_V']=row['voutn_V']-row['input_vcm_V']
   for key in ['sensitivity_cp_mV_per_pF','sensitivity_cn_mV_per_pF','sensitivity_delta_mV_per_pF']:
    z=arrays[key][i,j];row[key]=float(z) if np.isfinite(z) else None
 np.savez_compressed(O/f'cfb_{cf}_grid.npz',cp_pF=x,cn_pF=x,**arrays)
 grid[cf]=arrays
 summary[cf]={'cases':len(sub),'completed':sum(r['complete'] for r in sub),'settled':sum(r['settled'] for r in sub),'unsettled':sum(r['complete'] and not r['settled'] for r in sub),'failed':sum(not r['complete'] for r in sub),'output_rail_excursion_cases':sum(r.get('output_rail_excursion',False) for r in sub),'ranges':{k:[float(np.nanmin(np.where(valid,v,np.nan))),float(np.nanmax(np.where(valid,v,np.nan)))] for k,v in arrays.items() if k!='valid' and np.isfinite(np.where(valid,v,np.nan)).any()},'at_CP_CN_10pF':{k:(float(v[18,18]) if np.isfinite(v[18,18]) else None) for k,v in arrays.items() if k!='valid'},'center_CP_CN_6p5pF':{k:(float(v[11,11]) if np.isfinite(v[11,11]) else None) for k,v in arrays.items() if k!='valid'}}
 fig,axs=plt.subplots(2,3,figsize=(13.5,8.2),layout='constrained')
 titles=[('vdiff_V','VOUTP − VOUTN (V)'),('sensitivity_cp_mV_per_pF','Sensitivity to CP, CN fixed (mV/pF)'),('input_vcm_V','Input common mode (V)'),('output_vcm_V','Output common mode (V)'),('voutp_V','VOUTP (V)'),('voutn_V','VOUTN (V)')]
 for ax,(key,label) in zip(axs.flat,titles):
  data=np.where(valid,arrays[key],np.nan).T
  im=ax.imshow(data,origin='lower',extent=[.75,12.25,.75,12.25],aspect='equal',cmap='coolwarm' if key=='vdiff_V' else 'viridis')
  ax.set_xlabel('CP (pF)');ax.set_ylabel('CN (pF)');ax.set_title(label);fig.colorbar(im,ax=ax,shrink=.8)
 fig.suptitle(LABEL+f'CFB nominal {cf} pF — five 20 µm PMOS fingers, L={202.7*cf/40:g} µm\n5 V, 27 °C; recorded RTL phase replay; sample_valid measurement; unsettled/failed cells masked')
 fig.savefig(O/f'cfb_{cf}_measurements.png');fig.savefig(O/f'cfb_{cf}_measurements.pdf');plt.close(fig)
 fig,axs=plt.subplots(1,3,figsize=(13.5,4.4),layout='constrained')
 for ax,key,label in zip(axs,['sensitivity_cp_mV_per_pF','sensitivity_cn_mV_per_pF','sensitivity_delta_mV_per_pF'],['dVdiff/dCP, CN fixed','dVdiff/dCN, CP fixed','dVdiff/d(CP−CN), mean C fixed']):
  im=ax.imshow(arrays[key].T,origin='lower',extent=[.75,12.25,.75,12.25],aspect='equal',cmap='viridis')
  ax.set_xlabel('CP (pF)');ax.set_ylabel('CN (pF)');ax.set_title(label+'\n(mV/pF)');fig.colorbar(im,ax=ax,shrink=.8)
 fig.suptitle(LABEL+f'CFB nominal {cf} pF — sensitivity definitions')
 fig.savefig(O/f'cfb_{cf}_sensitivity.png');fig.savefig(O/f'cfb_{cf}_sensitivity.pdf');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
for cf in [40,50,60]:
 for cn,style in [(1,':'),(6,'-'),(12,'--')]:
  j=int((cn-1)/.5);v=grid[cf]['vdiff_V'][:,j];v=np.where(grid[cf]['valid'][:,j],v,np.nan)
  ax[0].plot(x,v*1000,style,label=f'CFB {cf}, CN {cn} pF')
 # Fixed mean C=6.5pF uses the anti-diagonal CP+CN=13.
 vals=np.array([grid[cf]['vdiff_V'][i,22-i] if grid[cf]['valid'][i,22-i] else np.nan for i in range(23)])
 ax[1].plot(2*x-13,vals*1000,'o-',ms=3,label=f'CFB {cf} pF')
ax[0].set_xlabel('CP (pF)');ax[0].set_ylabel('Differential output (mV)');ax[0].legend(fontsize=7,ncol=2)
ax[1].set_xlabel('CP − CN (pF), mean C = 6.5 pF');ax[1].set_ylabel('Differential output (mV)');ax[1].legend()
for a in ax:a.grid(alpha=.25)
fig.savefig(O/'feedback_comparison.png');fig.savefig(O/'feedback_comparison.pdf');plt.close(fig)
# Plain numeric data table; NaN means no valid derivative/measurement.
keys=['cfb_nominal_pF','cp_pF','cn_pF','delta_c_pF','mean_c_pF','voutp_V','voutn_V','vdiff_V','input_vcm_V','output_vcm_V','sensitivity_cp_mV_per_pF','sensitivity_cn_mV_per_pF','sensitivity_delta_mV_per_pF','cycle_drift_V','local_vdiff_slope_V_per_us','cycles','sample_us']
ordered=sorted(rows,key=lambda r:(r['cfb_nominal_pF'],r['cp_pF'],r['cn_pF']))
np.savetxt(O/'measurements.dat',np.array([[float(r.get(k)) if r.get(k) is not None else np.nan for k in keys]+[int(r['complete']),int(r['settled'])] for r in ordered]),header=' '.join(keys+['complete','settled']),fmt='%.12g')
(O/'measurements.json').write_text(json.dumps(ordered,indent=2,allow_nan=False));(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
