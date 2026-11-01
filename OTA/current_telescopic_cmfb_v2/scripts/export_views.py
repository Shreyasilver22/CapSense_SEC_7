from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1]
for f in ['designs','symbols','tb']:(R/f).mkdir(exist_ok=True)
text=(R/'models/layout_C.spice').read_text().replace('.subckt ota_telescopic_layout ','.subckt ota_telescopic_cmfb_v2 ')
(R/'models/ota_cmfb_v2_C.spice').write_text(text)
ports=['INP','INN','OUTP','OUTM','VDD','VSS','IREF','VCM','VBN','VBP']
sym=['v {xschem version=3.4.4 file_version=1.2}','G {}','K {type=subcircuit\nformat="@name @pinlist ota_telescopic_cmfb_v2"\ntemplate="name=XOTA"}','V {}','S {}','E {}','B 4 -90 -130 90 130 {}','T {@name} -75 -160 0 0 0.25 0.25 {}','T {SCL800 telescopic\nCMFB revision 2} -65 -10 0 0 0.23 0.23 {}']
coords=[(-110,-90),(-110,-60),(110,-90),(110,-60),(0,-150),(0,150),(-110,20),(-110,55),(-110,90),(-110,120)]
for k,(n,(x,y)) in enumerate(zip(ports,coords),1):
 ex=-90 if x<0 else 90 if x>0 else x;ey=-130 if y==-150 else 130 if y==150 else y
 sym += [f'L 4 {x} {y} {ex} {ey} {{}}',f'B 5 {x-2.5} {y-2.5} {x+2.5} {y+2.5} {{name={n} dir=inout pinnumber={k}}}',f'T {{{n}}} {ex+5 if x<0 else ex-65 if x>0 else 8} {ey-10} 0 0 0.15 0.15 {{}}']
(R/'symbols/ota_cmfb_v2.sym').write_text('\n'.join(sym).replace('K {type=subcircuit','K {type=subcircuit\nspice_primitive=true')+'\n')
res=['v {xschem version=3.4.4 file_version=1.2}','G {}','K {type=subcircuit\nformat="@name @pinlist RPP W=@w L=@l"\ntemplate="name=XR w=2.4u l=17142.857143u"}','V {}','S {}','E {}','B 4 -20 -8 20 8 {}','L 4 -30 0 -20 0 {}','L 4 20 0 30 0 {}','B 5 -32.5 -2.5 -27.5 2.5 {name=A dir=inout}','B 5 27.5 -2.5 32.5 2.5 {name=B dir=inout}','T {@name: RPP 200k} -35 -25 0 0 0.2 0.2 {}']
(R/'symbols/scl08_rpp_cmfb.sym').write_text('\n'.join(res).replace('K {type=subcircuit','K {type=subcircuit\nspice_primitive=true')+'\n')
head=['v {xschem version=3.4.4 file_version=1.2}','G {}','K {}','V {}','S {}','E {}'];lines=head.copy();idx=0
def wire(x1,y1,x2,y2,n):lines.append(f'N {x1} {y1} {x2} {y2} {{lab={n}}}')
def label(x,y,n):
 global idx
 idx+=1;lines.append(f'C {{devices/lab_pin.sym}} {x} {y} 0 0 {{name=L{idx} lab={n}}}')
pos={'MP1':(220,100),'MP2':(520,100),'MPC1':(220,250),'MPC2':(520,250),'MNC1':(220,400),'MNC2':(520,400),'MN1':(220,550),'MN2':(520,550),'MTAIL':(370,740),'MREF':(70,740),'MSP':(900,120),'MSM':(1200,120),'MSR':(1500,120),'MSIP':(900,320),'MSIM':(1200,320),'MSIR':(1500,320),'MCBI':(900,800),'MCBN':(900,1000),'MCT':(1250,720),'MCS':(1150,920),'MCR':(1450,920),'MCFN1':(1150,1120),'MCFN3':(1450,1120),'MCFN4':(1750,1120),'MCFP1':(1750,920),'MCFP2':(2050,920),'MCFN2':(2050,1120),'MCC':(2100,140),'MCM1':(2100,340),'MCM2':(2100,540)}
for line in (R/'models/schematic.spice').read_text().splitlines():
 a=line.split()
 if not a or not a[0].startswith('M'):continue
 nm=a[0];d,g,s,b=a[1:5];typ=a[5];x,y=pos[nm]
 par=dict(t.split('=',1) for t in a[6:] if '=' in t);w=par.get('W',par.get('w'));l=par.get('L',par.get('l'));m=par.get('M',par.get('m','1'));extra=' '.join(t for t in a[6:] if not re.match(r'^[WwLlMm]=',t))
 lines.append(f'C {{devices/{"nmos4" if typ=="N" else "pmos4"}.sym}} {x} {y} 0 0 {{name={nm} model={typ} w={w} l={l} m={m} extra="{extra}" hide_texts=true}}')
 lines.append(f'T {{{nm}: {w}/{l} x{m}}} {x-65} {y+70} 0 0 0.18 0.18 {{}}')
 for px,py,ex,ey,net in [(x-20,y,x-70,y,g),(x+20,y,x+85,y,b)]:wire(px,py,ex,ey,net);label(ex,ey,net)
 for sign,net in [(-1,d if typ=='N' else s),(1,s if typ=='N' else d)]:wire(x+20,y+sign*30,x+20,y+sign*55,net);label(x+20,y+sign*55,net)
for x in [240,540]:
 for y1,y2,n in [(155,195,'PX1' if x==240 else 'PX2'),(305,345,'OUTM' if x==240 else 'OUTP'),(455,495,'NX1' if x==240 else 'NX2'),(605,670,'TAIL')]:wire(x,y1,x,y2,n)
wire(240,670,540,670,'TAIL');wire(390,670,390,685,'TAIL')
for x,n in [(920,'SP'),(1220,'SM'),(1520,'SR')]:wire(x,175,x,265,n)
for x,nm,net in [(900,'XSP','SP'),(1200,'XSM','SM')]:
 lines.append(f'C {{scl08_rpp_cmfb.sym}} {x} 520 0 0 {{name={nm} w=2.4u l=17142.857143u}}');wire(x-30,520,x-70,520,net);label(x-70,520,net);wire(x+30,520,x+80,520,'SENSE');label(x+80,520,'SENSE')
wire(1270,775,1270,810,'CT');wire(1170,810,1470,810,'CT');wire(1170,810,1170,865,'CT');wire(1470,810,1470,865,'CT')
wire(1170,975,1170,1065,'CA');wire(1470,975,1470,1065,'RCM')
for k,n in enumerate(ports):lines.append(f'C {{devices/iopin.sym}} -180 {80+k*60} 0 0 {{name=P{k} lab={n}}}')
for txt,x,y in [('SCL800 telescopic OTA: unchanged signal core',20,-30),('NMOS sensing buffers + 200k averaging',800,-30),('CMFB error amplifier and mirror level shift',800,620),('MOS compensation',1950,-30)]:lines.append(f'T {{{txt}}} {x} {y} 0 0 0.35 0.35 {{}}')
lines += ['T {IREF=3.5uA; VBN=2.4V; VBP=VDD-2.2V; VCM=VDD/2.\nDrawing is the transistor schematic; simulate supplied extracted macro for layout results.\nSignal labels join repeated nodes. Resistor layout uses 40 series sections per 200k bank.} 20 1250 0 0 0.25 0.25 {}']
(R/'designs/ota_telescopic_layout.sch').write_text('\n'.join(lines)+'\n')
(R/'xschemrc').write_text('set CMFB_PROJECT_DIR [file normalize [file dirname [info script]]]\nset XSCHEM_LIBRARY_PATH "/usr/share/xschem/xschem_library:$CMFB_PROJECT_DIR/symbols"\nset netlist_dir [file join $CMFB_PROJECT_DIR tb]\nset USER_CONF_DIR [file join $CMFB_PROJECT_DIR .xschem]\nfile mkdir $USER_CONF_DIR\n')
# SC testbench: visible reusable OTA symbol, unchanged SC network/controls in a code block.
rows=json.loads((R/'SC_validation.json').read_text());r=next(x for x in rows if x['arch']=='layout_C' and x['switch']=='tg' and x['fs_Hz']==50000 and x['dt_ns']==10 and x['delta_pF']==0 and x['VDD']==5 and x['load_pF']==5)
code=(R/'results'/r['name']/'tb.cir').read_text().splitlines()[1:]
code=[x for x in code if not x.startswith('XOTA ') and x!='.end'];code='\n'.join(code).replace(str(R/'models/layout_C.spice'),'../models/ota_cmfb_v2_C.spice').replace('wrdata transient.dat','wrdata xschem_SC.dat').replace('"','\\"')
sch=head.copy()+['C {ota_cmfb_v2.sym} 400 300 0 0 {name=XOTA}']
for (n,(x,y)),net in zip(zip(ports,coords),['ref','sum','out','other','vdd','0','bias','vcm','vbn','vbp']):sch.append(f'C {{devices/lab_pin.sym}} {400+x} {300+y} 0 0 {{name=PIN_{n} lab={net}}}')
sch += [f'C {{devices/code.sym}} 700 100 0 0 {{name=SC_network only_toplevel=false value="{code}"}}','T {Verified-layout OTA symbol in the original SC testbench\nDouble-click SC_network for the capacitor, switch, clock and analysis definitions.\nModel includes and output data are relative to the tb directory.} 100 520 0 0 0.3 0.3 {}']
(R/'designs/sc_ota_cmfb_v2.sch').write_text('\n'.join(sch)+'\n')
