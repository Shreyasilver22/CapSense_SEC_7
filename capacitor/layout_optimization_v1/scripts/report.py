from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--ota-project',type=Path);a=p.parse_args();cs=json.loads((R/'results/catalog.json').read_text())['capacitors'];geo=json.loads((R/'results/geometry.json').read_text());targets=['3p','4p','8p'];styles=['baseline','compact','slotted']
fig,axs=plt.subplots(3,3,figsize=(12,12))
for row,t in enumerate(targets):
 b=next(x for x in cs if x['style']=='baseline' and x['token']==t)
 for col,style in enumerate(styles):
  c=next(x for x in cs if x['style']==style and x['token']==t);g=next(x for x in geo if x['name']==c['name']);ax=axs[row,col]
  for outlines,color in zip(g['polygons'],['royalblue','orange']):
   for poly in outlines:ax.add_patch(Polygon(poly,closed=True,facecolor=color,alpha=.48,edgecolor='none'))
  ax.set(xlim=(-15,b['width_um']+5),ylim=(-15,b['height_um']+5),aspect='equal',xlabel='um',ylabel='um',title=f"{style}, target {t}\nCm={c['Cmut_F']*1e12:.4f} pF, area={c['area_um2']/1e6:.3f} mm2")
fig.suptitle('Identical physical scale across each row: Metal 1 blue, Metal 2 orange',fontsize=12);fig.tight_layout(rect=(0,0,1,.97));fig.savefig(R/'plots/layout_comparison.png',dpi=180);fig.savefig(R/'plots/layout_comparison.pdf');plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(14,4));colors=['C0','C1','C2'];x=np.arange(3);width=.25
for i,style in enumerate(styles):
 cells=[next(c for c in cs if c['style']==style and c['token']==t) for t in targets]
 for ax,key,factor in [(axs[0],'Ctop_sub_F',1e12),(axs[1],'Cbot_sub_F',1e12),(axs[2],'area_um2',1e-6)]:ax.bar(x+(i-1)*width,[c[key]*factor for c in cells],width,label=style,color=colors[i])
for ax,label,title in zip(axs,['pF','pF','mm2'],['TOP to substrate','BOT to substrate','Bounding layout area']):ax.set(xticks=x,xticklabels=targets,ylabel=label,title=title);ax.grid(axis='y',alpha=.25);ax.legend(fontsize=8)
fig.tight_layout();fig.savefig(R/'plots/parasitic_comparison.png',dpi=180);fig.savefig(R/'plots/parasitic_comparison.pdf');plt.close(fig)
text='# Matched-capacitance layout comparison\n\nAll values are experimental raw-.ext estimates. Useful capacitances match each baseline within 0.13%; unchanged extraction deck/conditions. No physical matching or tolerance claim.\n\n| Target | Layout | Mutual C (pF) | TOP-sub (pF) | BOT-sub (pF) | Area (mm2) | M1 route R proxy (ohm) |\n|---|---|---:|---:|---:|---:|---:|\n'
for c in cs:text+=f"| {c['token']} | {c['style']} | {c['Cmut_F']*1e12:.5f} | {c['Ctop_sub_F']*1e12:.5f} | {c['Cbot_sub_F']*1e12:.5f} | {c['area_um2']/1e6:.5f} | {c['M1_route_R_proxy_ohm']:.2f} |\n"
b=next(c for c in cs if c['name']=='capopt_baseline_4p');s=next(c for c in cs if c['name']=='capopt_slotted_4p');text+='\nFor the same ~4 pF mutual capacitance, slotted versus baseline reductions:\n\n'
for k,label in [('Ctop_sub_F','TOP substrate loading'),('Cbot_sub_F','BOT substrate loading'),('area_um2','Footprint')]:text+=f'- {label}: {100*(1-s[k]/b[k]):.2f}%\n'
text+='\nThe routing-resistance column is a geometry/sheet-resistance proxy, not PEX. It excludes broad-plate distributed resistance, coupling, contacts, vias and frequency effects. It was not included in the OTA model. Compact routing is narrower and has a slightly larger proxy than the baseline despite smaller area.\n\nSlotted geometry uses corresponding 20 um wide strips separated by 2 um slots, connected by separate 3 um side spines, rather than individual routed tiles. The lower metal signal plate shields much of the upper plate from substrate in the extraction model; no extra grounded shield or process layer is added. Less terminal/bus metal and fewer plate edges also contribute. The old extractor and simplified capacitance coefficients limit confidence in absolute and relative numbers; independent supported extraction is still required.\n'
(R/'RESULTS.md').write_text(text)
if a.ota_project:
 O=a.ota_project.resolve();j=json.loads((O/'results/summary.json').read_text());fig,axs=plt.subplots(2,2,figsize=(12,8));names=['capopt_baseline_8p','capopt_baseline_4p','capopt_compact_4p','capopt_slotted_4p']
 for name in names:
  data=np.loadtxt(O/'results'/name/'ac_cl5_vc2.5/ac.dat',skiprows=1);t=np.loadtxt(O/'results'/name/'tran_cl5_large/tran.dat',skiprows=1);r=next(x for x in j['nominal'] if x['name']==name)
  axs[0,0].semilogx(data[:,0],data[:,1],label=name);axs[0,1].semilogx(data[:,0],data[:,2],label=name);axs[1,0].plot(t[:,0]*1e6,t[:,2],label=name);axs[1,1].scatter(r['UGF_MHz'],r['minimum_PM_deg'],s=65,label=name)
 axs[0,0].set(xlabel='Frequency (Hz)',ylabel='Gain (dB)',xlim=(1,1e8));axs[0,1].set(xlabel='Frequency (Hz)',ylabel='Phase (degrees)',xlim=(1e3,1e8));axs[1,0].set(xlabel='Time (us)',ylabel='Output (V)',xlim=(9,22),title='2 V follower step, explicit CL=5 pF');axs[1,1].set(xlabel='Nominal UGF (MHz)',ylabel='Minimum checked PM (degrees)');axs[1,1].axhline(60,color='k',ls='--')
 for ax in axs.flat:ax.grid(alpha=.25);ax.legend(fontsize=7)
 fig.tight_layout();fig.savefig(O/'plots/ota_comparison.png',dpi=180);fig.savefig(O/'plots/ota_comparison.pdf');plt.close(fig)
 rows='| Capacitor | UGF (MHz) | Nominal PM (deg) | Min checked PM (deg) | 100 mV settling (us) | 2 V settling (us) |\n|---|---:|---:|---:|---:|---:|\n'
 for r in j['nominal']:rows+=f"| {r['name']} | {r['UGF_MHz']:.3f} | {r['PM_deg']:.2f} | {r['minimum_PM_deg']:.2f} | {r['small_settling_us']:.3f} | {r['large_settling_us']:.3f} |\n"
 (O/'RESULTS.md').write_text('# OTA comparison with layout-derived capacitor models\n\n'+rows+'\nSettling is 0.1% of step amplitude around actual final output, worst polarity, 5 ns max timestep. Static error (~-0.206 mV for the small step) is separate. All cases retain the same transistor geometry, 2.5 uA ideal reference, 5 V, 27 C, TOP=n2/BOT=out/SUB=vss. Min PM spans CL1/5/10 pF x follower bias1.5/2.5/3.5 V. The 81 AC and 54 base transient runs are nominal-deck continuous-time follower checks, not PVT or an SC system simulation. Models omit routing resistance and all unresolved extraction/model limitations remain.\n')
 print('OTA plots/results written')
print('Capacitor layout plots/results written')
