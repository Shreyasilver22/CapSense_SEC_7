from pathlib import Path
import re,subprocess,tempfile,json,hashlib,sys
R=Path(__file__).resolve().parents[1]
TECH=Path('/home/berson_meshak/pdk/scl08/analog_pdk/Open_Source_SCL_0.8micron_PDK/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/magic/SCL_CP8D.tech')
text=TECH.read_text();start=text.index('cifinput');end=text.index('\nend',start);part=text[start:end];removed=[]
for name in ['nwell_rev','boron_rev','boron','CONT','respin']:
 pattern=r'(?m)^layer '+name+r' .*?(?=^layer |^calma |\Z)'
 part,n=re.subn(pattern,'',part,flags=re.S);assert n==1,(name,n);removed.append(name)
text=text[:start]+part+text[end:]
text=text.replace('allpolynonfet    *poly','allpolynonfet    *poly,*mrp1,*mrp2')
tcl='''crashbackups stop
drc off
gds read ../layout/ota_telescopic_layout.gds
load ota_telescopic_layout
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice resistor tee on
ext2spice subcircuits top on
ext2spice -o ota_C_raw.spice
puts "Extraction feedback count: [feedback count]"
for {set i 1} {$i <= [feedback count]} {incr i} {feedback find $i; feedback why}
quit -noprompt
'''
(R/'pex/extract_C.tcl').write_text(tcl)
rc='--rc' in sys.argv
work=R/'pex'
if rc:
 work=work/'rc_diagnostic';work.mkdir(exist_ok=True)
 tcl=tcl.replace('../layout/','../../layout/').replace('extract all','extresist threshold 0\nextresist minres 10\nextresist mindelay 0\nextract do resistance\nextract all').replace('ext2spice subcircuits','ext2spice extresist on\next2spice subcircuits').replace('ota_C_raw.spice','ota_RC_raw.spice')
(work/'extract.tcl').write_text(tcl)
with tempfile.TemporaryDirectory(prefix='scl08_extract_') as tmp:
 p=Path(tmp)/'SCL_CP8D.tech';p.write_text(text)
 run=subprocess.run(['/tmp/magic_ota_tool/bin/magic','-dnull','-noconsole','-norcfile','-T',str(p),'extract.tcl'],cwd=work,capture_output=True,text=True,timeout=240)
 log=run.stdout+run.stderr;(work/'extract_C.log').write_text(log);assert run.returncode==0,log[-3000:]
meta=dict(tool='Magic 8.3.688',original_tech_sha256=hashlib.sha256(TECH.read_bytes()).hexdigest(),original_tech_unmodified=True,raw_marker_paint_omitted=removed,poly_resistor_body_cap_alias=True,limits='Extraction-only adaptations as in prior OTA study; not foundry-qualified. C-only extraction; no claim of full wire/well/substrate RC verification.')
meta.update(RC_attempt=rc,substrate_tile_errors=len(re.findall('Substrate tile',log)),missing_substrate_connections=len(re.findall('Missing substrate connection',log)))
(R/'verification'/('RC_setup.json' if rc else 'extraction_setup.json')).write_text(json.dumps(meta,indent=2));print(log[-3000:])
