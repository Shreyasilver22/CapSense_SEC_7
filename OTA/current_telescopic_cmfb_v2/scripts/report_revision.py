from pathlib import Path
import os,json,hashlib,csv
os.environ.setdefault('MPLCONFIGDIR','/tmp/cmfb_revision_mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
import sweep as w
R=w.R;OLD=R.parent/'telescopic_layout_20261101'
load=lambda p:json.loads((R/p).read_text())
acs=load('extracted_ac.json')+load('reset_range_ac.json');sc=load('SC_validation.json');prev=load('previous_control.json')[0];cfg=load('selected.json');geometry=load('verification/geometry_summary.json');oldgeo=json.loads((OLD/'verification/geometry_summary.json').read_text());oldexport=json.loads((OLD/'verification/model_export.json').read_text());exp=load('verification/model_export.json');ver=load('verification/summary.json');views=load('verification/views.json');rc=load('verification/RC_setup.json')
def sel(arch='layout_C',switch='tg',fs=50000,dt=10,delta=0,vdd=5,load=5):return next(x for x in sc if x['arch']==arch and x['switch']==switch and x['fs_Hz']==fs and x['dt_ns']==dt and x['delta_pF']==delta and x['VDD']==vdd and x['load_pF']==load)
nom=sel();smooth=sel(switch='smooth');fine=sel(dt=2);delta=sel(dt=2,delta=.05);measured=(delta['last_out_V']-fine['last_out_V'])*1000
nomac={k:next(x for x in acs if x['kind']==k and x['mos']=='tntp49_5v' and x['VDD']==5 and x['temp']==27 and x['res']=='typ' and x['vd']==0 and x['CL_pF']==5) for k in ['cm','diff']}
worst={k:min((x for x in acs if x['kind']==k and x['status']=='OK' and x['PM_deg'] is not None),key=lambda x:x['PM_deg']) for k in ['cm','diff']}
status=dict(DRC_markers=ver['DRC_markers'],LVS=ver['LVS_match'],extracted_topology_LVS=exp['topology_LVS'],xschem=views,signal_core_unchanged=True,AC_cases=len(acs),AC_execution_failures=sum(x['status']!='OK' for x in acs),CMFB_nominal_PM_deg=nomac['cm']['PM_deg'],CMFB_worst_PM_deg=worst['cm']['PM_deg'],signal_worst_PM_deg=worst['diff']['PM_deg'],all_tested_CMFB_cases_above_60=all(x['status']=='OK' and x.get('PM_deg') is not None and x['PM_deg']>=60 for x in acs if x['kind']=='cm'),nominal_differential_gain_dB=nomac['diff']['gain_dB'],nominal_differential_UGF_MHz=max(x['f_MHz'] for x in nomac['diff']['crossings']),layout_area_mm2=geometry['area_mm2'],resistor_body_ground_C_pF=exp['resistor_body_ground_C_pF'],SC_cases=len(sc),SC_execution_failures=sum(x['status']!='OK' for x in sc),nominal_SC_TG_output_V=nom['last_out_V'],nominal_SC_TG_error_mV=nom['max_sample_error_mV'],nominal_SC_CM_error_mV=nom['max_CM_error_mV'],nominal_SC_power_uW=nom['avg_VDD_power_uW'],sensor_delta_50fF_response_mV=measured,full_RC_qualified=False,noise_qualified=False,limits='Engineering capacitance extraction; resistor-body alias unqualified; full RC substrate errors remain. SC uses Gear; ideal diagnostic control is smoothed; original abrupt ideal switch fails convergence.')
(R/'verification/final_status.json').write_text(json.dumps(status,indent=2))
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.22})
def data(root,x):return np.loadtxt(root/'results'/x['name']/'transient.dat',skiprows=1)
fig,ax=plt.subplots(2,1,figsize=(11,8),sharex=True)
for x,label,color in [(prev,'Previous extracted layout','#c94c4c'),(nom,'Revised extracted layout','#168960')]:
 d=data(R,x);t=d[:,0]*1e6;ax[0].plot(t,d[:,1],label=label,color=color);ax[1].plot(t,((d[:,1]+d[:,3])/2-2.5)*1000,color=color)
ax[0].set(ylabel='SC output (V)',title='Same transistor-switch SC circuit and Gear solver, 50 kHz, 5 V, 27 C');ax[0].legend();ax[1].set(ylabel='Output common-mode error (mV)',xlabel='Time (us)',xlim=(45,205))
fig.tight_layout();fig.savefig(R/'plots/SC_before_after.png',dpi=170);fig.savefig(R/'plots/SC_before_after.pdf');plt.close(fig)
fig,ax=plt.subplots(2,1,figsize=(10,7),sharex=True)
for p,label,color in [(OLD/'results/cmfb_layout_C/ac.dat','Previous layout','#c94c4c'),(R/'results/extracted/cm_0_tntp49_5v_5_27_5_2.4_typ/ac.dat','Revised layout','#168960')]:
 d=np.loadtxt(p,skiprows=1);h=d[:,1]+1j*d[:,2];ax[0].semilogx(d[:,0],20*np.log10(abs(h)),label=label,color=color);ax[1].semilogx(d[:,0],np.unwrap(np.angle(h))*180/np.pi,color=color)
ax[0].set(ylabel='CMFB loop magnitude (dB)',title='Extracted-capacitance CMFB loop: instability removed in the revised model');ax[0].axhline(0,color='grey',ls='--');ax[0].legend();ax[1].set(ylabel='CMFB loop phase (degrees)',xlabel='Frequency (Hz)',xlim=(100,1e7));ax[1].axhline(-180,color='grey',ls='--')
fig.tight_layout();fig.savefig(R/'plots/CMFB_before_after.png',dpi=170);fig.savefig(R/'plots/CMFB_before_after.pdf');plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(11,4.5))
for sw,label,color in [('smooth','Smoothed ideal control','#168960'),('tg','Native transistor switches','#296eac')]:
 a=[sel(switch=sw,fs=f) for f in [50000,100000,200000]];ax[0].plot([x['fs_Hz']/1000 for x in a],[(x['last_out_V']-3.3)*1000 for x in a],'o-',label=label,color=color)
ax[0].set(xlabel='Clock (kHz)',ylabel='Third sample error (mV)',title='Raw offset and settling remain separate',xticks=[50,100,200]);ax[0].legend(fontsize=8)
ax[1].bar(['Previous','Revised'],[oldgeo['area_mm2'],geometry['area_mm2']],color=['#c94c4c','#168960']);ax[1].set(ylabel='Bounding area (mm2)',title='Actual first-pass GDS bounding area')
fig.tight_layout();fig.savefig(R/'plots/tradeoffs.png',dpi=170);fig.savefig(R/'plots/tradeoffs.pdf');plt.close(fig)
rects=load('verification/geometry.json');palette={1:'#f2c273',2:'#57966a',3:'#f4da9c',4:'#c1534d',5:'#e0a49a',6:'#e6b4ae',7:'#222222',8:'#467fc2',9:'#252953',10:'#9271b4',36:'#c18c40',44:'#d77928'}
fig,ax=plt.subplots(figsize=(9,10))
for layer in [1,3,5,6,2,4,44,36,10,8,7,9]:
 boxes=[Rectangle((x1,y1),x2-x1,y2-y1) for la,x1,y1,x2,y2 in rects if la==layer]
 if boxes:ax.add_collection(PatchCollection(boxes,facecolor=palette[layer],edgecolor='none',alpha=.5 if layer in [1,3,5,6,10] else .85,rasterized=True))
ax.set_aspect('equal');ax.set(xlim=(-20,1090),ylim=(-20,1250),xlabel='um',ylabel='um',title=f'Revised physical OTA + CMFB: {geometry["area_mm2"]:.3f} mm2 bounding box')
ax.text(600,1080,'Two 200 kohm P-poly banks\n40 sections per bank',ha='center',bbox=dict(facecolor='white',alpha=.8,edgecolor='none'))
fig.tight_layout();fig.savefig(R/'plots/layout.png',dpi=180);fig.savefig(R/'plots/layout.pdf');plt.close(fig)

# Portable SPICE files; canonical simulator model for a single candidate.
for a in ['schematic','layout_C']:
 for sw in ['smooth','tg']:
  x=sel(arch=a,switch=sw);text=(R/'results'/x['name']/'tb.cir').read_text().replace(str(R/'models'/f'{a}.spice'),f'../models/{a}.spice').replace('wrdata transient.dat',f'wrdata {a}_{sw}.dat');(R/'tb'/f'{a}_{sw}.cir').write_text(text)
num=[]
for sw in ['smooth','tg']:
 a=sel(switch=sw);b=sel(switch=sw,dt=2);num.append(dict(switch=sw,third_output_10ns_V=a['last_out_V'],third_output_2ns_V=b['last_out_V'],difference_uV=(b['last_out_V']-a['last_out_V'])*1e6))
w.save('numerical_timestep',num)
coreac_rows=[dict(kind=k,nominal_PM_deg=nomac[k]['PM_deg'],worst_PM_deg=worst[k]['PM_deg'],worst_configuration=worst[k]) for k in ['cm','diff']];w.save('loop_summary',coreac_rows)
table='| Condition | Switch control | Last third sample (V) | Worst sampled output error (mV) | Worst sampled CM error (mV) |\n|---|---|---:|---:|---:|\n'
for x in [sel(switch=sw,fs=f) for f in [50000,100000,200000] for sw in ['smooth','tg']]+[sel(switch=sw,vdd=v) for v in [4.5,5.5] for sw in ['smooth','tg']]:
 table+=f"| {x['VDD']} V, {x['temp']} C, {x['fs_Hz']/1000:g} kHz | {x['switch']} | {x['last_out_V']:.6f} | {x['max_sample_error_mV']:.3f} | {x['max_CM_error_mV']:.3f} |\n"
R.joinpath('README.md').write_text(f'''# Telescopic OTA — CMFB revision 2, 1 November 2026

The CMFB was redesigned, laid out, checked and actually re-simulated in ngspice with extracted capacitance. The revised model has stable nominal SC behavior and meets the previous60-degree feedback-loop screening target throughout the tested AC grid. This is an improved prototype, not a final optimum or tapeout-qualified ASIC design.

## What changed

- Averaging resistance: **1 Mohm ->200 kohm per branch**. Native SCL08 RPP geometry and electrical model retained.
- Sensing: replaced the PMOS source followers and PMOS bias branches with **four W20/L1.6 NMOS followers per channel and two W20/L3.2 NMOS sink units per channel**, roughly7 uA nominal per channel. These include a matched reference follower.
- Detector: PMOS differential error pair, with NMOS/PMOS current mirrors translating its output current into the high-voltage PC control node. The PMOS input pair usesW5/L2.4; mirror unitsW10/L3.2; its tail is approximately1 uA. This avoids requiring a low-voltage detector output to drivePC directly. It also avoids the large-area PMOS sensing/bias devices tested as an alternative.
- Compensation: **12 PMOS W20/L10 units fromPC to each output**, plus the existing four units fromPC toVDD. Controller current and compensation were selected together; this increases intentional output loading relative to the first8-unit prototype.
- Layout: shortened the resistor banks and placed the high-impedance detector near them. Resistors use40 sections per200 kohm bank, eachW2.4/L428.571 um. Signal-core transistor W/L, topology, IREF3.5 uA and external cascode bias values **remain unchanged**. The exported transistor schematic was separately checked againstGDS; `verification/views.json` records the unchanged nine signal-core devices.

Resistor/current/compensation trials, alternative PMOS headroom changes and NMOS sensing variants are preserved in their JSON/CSV records. The final choice is `selected.json`; rejected trial results are not qualification data for the final candidate. A clocked CMFB was not implemented because this continuous-time version recovered the stability target; it remains an alternative if final area/power requirements demand it.

## Physical and extraction results

| Item | Previous layout | Revised layout |
|---|---:|---:|
| Native RPP resistance, each branch |1 Mohm |200 kohm |
| Extracted engineering resistor-body ground C, both banks |{oldexport['resistor_body_ground_C_pF']:.2f} pF |{exp['resistor_body_ground_C_pF']:.2f} pF |
| GDS bounding area |{oldgeo['area_mm2']:.3f} mm2 |{geometry['area_mm2']:.3f} mm2 |
| Physical MOS units |43 |{geometry['MOS_units']} |
| RPP body sections |200 |{geometry['resistor_segments']} |
| Nominal CMFB phase margin |−48.73 degrees |{nomac['cm']['PM_deg']:.2f} degrees |

New GDS is `layout/ota_telescopic_layout.gds`. **Local SCL DRC:0 markers. LVS:MATCH**, with wrong-gate and wrong-width negative controls failing as expected. The repaired C-extracted model separately matches the GDS topology. These checks use the original unmodified local KLayout decks. Bounding area is an unoptimized macro floorplan, not a minimum die-area claim; density, matching, pad/ESD and full-chip signoff remain outside this check.

The model `models/layout_C.spice` includes{exp['total_explicit_cap_count']} explicit capacitances and native80-section resistor bodies exported as160 half-resistors. Native tee export drops a half for this PDK rsubckt type; both halves are restored from `.ext` terminals and geometry and independently checked by LVS. Do not simulate `pex/ota_C_raw.spice` as if it were complete.

## Extracted feedback-loop screening

**{len(acs)} AC cases completed, with no execution failures.** Five literal native MOS corner files; VDD4.5/5/5.5 V; temperature0/27/85 C; native best/typ/worst resistor models. Initial grid checks both common-mode and differential loops, center operation with1/10 pF per output, and output differential levels that cover the3.3 V integration endpoint. Extra reset-range tests cover output1.5 V and its complementary output up to4 V at5.5 V supply, CL10 pF, both polarities. Nominal CL5 pF points are also saved.

- Lowest tested CMFB margin: **{worst['cm']['PM_deg']:.2f} degrees**.
- Lowest tested differential-loop margin: **{worst['diff']['PM_deg']:.2f} degrees**.
- Nominal matched-model differential gain: **{nomac['diff']['gain_dB']:.2f} dB**.
- Nominal differential UGF: **{status['nominal_differential_UGF_MHz']:.3f} MHz**, CL5 pF on each output, input CM1.5 V and output CM2.5 V.

Every unity crossing is retained in the JSON and the minimum margin is used. CMFB is checked by symmetric sensing-gate injection with differential feedback closed. These are engineering loop diagnostics, not a formal multi-loop pole-count/Nyquist proof, continuous-range guarantee, or foundry-certified PVT qualification. The ranges remain project screening assumptions. Nominal frequency/gain figures describe the differential benchmark, not the bandwidth of the entire SC readout.

Static common-mode setpoint error reaches {max(abs(x['CM_error_mV']) for x in acs if x['status']=='OK'):.2f} mV at large output imbalance in the saved bias-point grid. Improved loop stability does not establish exact common-mode regulation; this residual must fit the future ADC/interface budget.

## Same SC circuit: measured behavior

CS2.5 pF,CF7.5 pF,VREF1.5 V,VP0.3 V, output and complementary-output loads5 pF, 50 us startup reset and two frames of three integration cycles. Capacitors, clock sequence/edges/nonoverlap, switch dimensions and sensor stimulus stay as before. Only the OTA macro is layout extracted; the SC network remains schematic-level. Ideal expected staircase:1.5->2.1->2.7->3.3 V.

Previous and revised extracted layouts were both run with the **same native transistor switches and Gear solver**. Prior worst sampled common-mode error was{prev['max_CM_error_mV']:.1f} mV; revised nominal error is**{nom['max_CM_error_mV']:.2f} mV**. Large common-mode oscillation is removed in the revised nominal trace. Gear does not hide the old instability: the previous layout still fails in that same-method control run.

{table}
At nominal50 kHz, the smooth100-ohm diagnostic control gives worst sampled error**{smooth['max_sample_error_mV']:.3f} mV**. The actual transistor-switch test retains about**{nom['max_sample_error_mV']:.2f} mV raw error**, dominated by switching/readout effects; the CMFB fix does not eliminate that error. Higher clocks still degrade settling: at100 kHz the smooth-control final error is about{abs(sel(switch='smooth',fs=100000)['last_out_V']-3.3)*1000:.2f} mV. At the selected4.5 V/85 C corner the50 kHz smooth-control error is about{sel(switch='smooth',vdd=4.5)['max_sample_error_mV']:.2f} mV. No final accuracy or clock-rate requirement has been established.

With a+50 fF sensor change, expected third-sample change is36 mV. The2 ns native-switch runs give**{measured:.6f} mV** after subtracting a matching2 ns zero-change run. This is offline baseline subtraction, not an implemented calibration circuit, ADC resolution claim or noise-limited sensitivity measurement.

Nominal modeled VDD power during SC operation is**{nom['avg_VDD_power_uW']:.1f} uW**, compared with about181.8 uW for the earlier schematic telescopic prototype. Increased sensing current is a real power cost. The unstable old layout's average power is not a useful efficiency baseline. External reference/clock drivers and a fabricated current/voltage-reference generator are excluded. The footprint remains much larger than the earlier simple two-stage OTA; this CMFB revision does not establish that telescopic is the optimum overall ASIC architecture.

## Numerical and model limits

The abrupt ideal SW control with extracted capacitances aborts with a timestep-too-small error at the firstphi2 event, with both trapezoidal and Gear attempts. Initial failed records are retained under`verification/numerical_trials/SC_aborted_trap.json` and raw result directories; those are not counted as successful final SC tests. Transistor switches converge with second-order Gear. For the ideal diagnostic only, a continuous conductance transitioning around the same clock threshold replaces the discontinuous SW element: Ron100 ohm, Roff1e12 ohm, tanh width0.025*VDD. The actual transistor-switch circuit and10 ns clocks are unchanged. Smooth-control results must be labeled as such; they are not a rerun of the original discontinuous ideal SW model.

Both smooth-control and transistor-switch nominal cases were repeated with2 ns maximum timestep. See`numerical_timestep.json`; adaptive grids and netlist ordering can change microvolt-scale values. The Xschem-symbol SC export was separately simulated and matches all six sampled native-deck outputs within**{views['max_sample_difference_uV']:.3f} uV**. The transistor schematic also separately matches GDS in local LVS.

This is **engineering capacitance extraction**, including intentional resistor-body resistance. It is not qualified full wire/contact/diffusion/well/substrate RC. As in the prior work, temporary extraction-only import filtering prevents raw non-electrical marker paint overwriting electrical well/active planes. Original PDK files are unchanged. The poly capacitance alias is extended to resistor-body paint using existing coefficients; this body-C estimate is not a foundry-qualified resistor extraction model. The exact10.64 pF needs process/extractor validation before treating it as a silicon prediction. Shorted-terminal MOS capacitor warnings are recorded and their intended four-terminal topology is independently checked.

Full RC extraction was attempted again and reports**{rc['substrate_tile_errors']} substrate-tile errors and{rc['missing_substrate_connections']} missing-substrate messages**. Its raw output under`pex/rc_diagnostic/` is excluded from performance claims. Existing native HSPICE-to-ngspice ignored-parameter/noise limitations remain. Noise, mismatch Monte Carlo, reference startup/noise, routed SC/switch/sensor parasitics and final fabrication qualification remain pending. MOS compensation is not evidence that MOS devices can replace precision SC/SAR capacitors.

## Reuse and reproduction

- `designs/ota_telescopic_layout.sch`: transistor schematic, organized into signal core, NMOS sensing buffers, mirror-level-shift controller and MOS compensation. Global signal labels join repeated nodes; visible core wiring shows the signal path.
- `symbols/ota_cmfb_v2.sym`: reusable10-pin Xschem symbol. Include `models/ota_cmfb_v2_C.spice` and your native MOS/RPP cards. This export has unique subcircuit name`ota_telescopic_cmfb_v2`; the verified GDS/reference top cell remains`ota_telescopic_layout` with the same pin order.
- Pin order:`INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP`. Integrated reference diode; IREF3.5 uA,VSS0,VBN2.4 V,VBP=VDD-2.2 V,VCM=VDD/2. VBN/VBP/VCM generators remain external ideal references in these tests.
- `designs/sc_ota_cmfb_v2.sch`: visible OTA symbol with the unchanged SC network and simulation controls in the code block. Start Xschem from this project directory to load`xschemrc`. Netlist into`tb` and run from`tb` so relative model includes resolve. PDK includes expect`/home/berson_meshak/pdk/scl08/ngspice_models49`; collaborators must point those includes at their own authorized PDK.
- `./open_xschem.sh` opens that symbol testbench with the project configuration and `tb` as its simulation directory. Run it from a normal WSL desktop terminal with Xschem display access.
- `tb/layout_C_tg.cir` and`layout_C_smooth.cir`: standalone nominal decks. Run`ngspice -b -o layout_C_tg.log layout_C_tg.cir` from`tb`. Native PDK cards are referenced, not redistributed.
- Regenerate in order: `scripts/prepare.py`; `klayout -b -r scripts/generate.py`; `scripts/verify.py`; `scripts/extract.py`; `scripts/export_models.py`; `scripts/validate_layout.py`; `scripts/check_reset_range.py`. Add`--sc-only` to validation to repeat SC tests without repeating AC. `scripts/export_views.py` writes schematic/symbol/testbench exports; `scripts/verify_views.py` verifies their generated data. Raw decks preserve original run paths; regenerate after relocation. The previous study's`scripts/rebuild_magic.py` and bundled source restore`/tmp/magic_ota_tool` if it is missing.
- Plots:`plots/SC_before_after.png`, `CMFB_before_after.png`, `tradeoffs.png`, `layout.png`, plus PDFs and native schematic SVG.

`verification/final_status.json`, `loop_summary.json`, `SC_validation.json`, `selected.json`, hashes and raw logs preserve the final evidence. Intermediate sweeps are exploratory results and do not replace the final extracted-model data. Next work is a qualified full-RC/noise flow and a system accuracy/power budget, then switching-error/settling optimization if this architecture remains the preferred ASIC option.
''')
hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['scripts','layout','models','schematic','symbols','designs','tb'] for p in (R/folder).glob('*') if p.is_file() and p.suffix not in ['.log','.dat']}
for name in ['selected.json','xschemrc','open_xschem.sh']:hashes[name]=hashlib.sha256((R/name).read_bytes()).hexdigest()
(R/'hashes.json').write_text(json.dumps(hashes,indent=2));print(json.dumps(status,indent=2));print(table)
