#!/usr/bin/env python3
"""Create an ignored, locally configured working copy without editing tracked sources."""
from pathlib import Path
import argparse, shutil, re, hashlib, json
ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdk-root', required=True, type=Path, help='Installed scl_cp8d directory, not an entire PDK installation to copy')
parser.add_argument('--runtime', type=Path, help='Optional existing private Icarus runtime directory containing bin/iverilog and lib/libvvp.so')
args = parser.parse_args()
pdk = args.pdk_root.expanduser().resolve()
assert (pdk/'libs.tech').is_dir(), 'Expected scl_cp8d/libs.tech under --pdk-root'
work = ROOT/'work'
assert not work.exists(), 'work/ already exists. Keep your edited schematics; use another checkout for a fresh setup.'
projects = ['Phase_Generator_Testbench', 'Integrated_Design']
for name in projects:
    shutil.copytree(ROOT/name, work/name)
tag = hashlib.sha256(str(work).encode()).hexdigest()[:10]
phase_alias = f'capsense_{tag}_phase_runtime'
integrated_alias = f'capsense_{tag}_integrated'
replacements = {
    '/home/shreyas/Desktop/Sec_7/Phase_Generator_Testbench': str(work/projects[0]),
    '/home/shreyas/Desktop/Sec_7/Integrated_Design': str(work/projects[1]),
    '/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d': str(pdk),
    '/tmp/capsense_phase_runtime': '/tmp/'+phase_alias,
    '/tmp/capsense_integrated': '/tmp/'+integrated_alias,
    "'capsense_phase_runtime'": repr(phase_alias),
    "'capsense_integrated'": repr(integrated_alias),
}
for file in work.rglob('*'):
    if file.is_file() and (file.suffix in {'.sch','.sym','.spice','.py','.sh','.tcl'} or file.name=='xschemrc'):
        text = file.read_text()
        for old,new in replacements.items(): text = text.replace(old,new)
        file.write_text(text)
# Older saved GUI revisions omitted these shared defaults. Put missing values
# in the VISIBLE schematic CAP_VALUES block, never in a hidden model file.
filled = []
for file in (work/'Integrated_Design/schematic').glob('capsense*.sch'):
    text = file.read_text()
    missing = [(k,v) for k,v in [('CS','10p'),('CFB_W','20u'),('CFB_M','5')] if not re.search(r'\b'+k+r'\s*=',text) and ('{'+k+'}' in text or '\\{'+k+'\\}' in text)]
    if missing:
        text,count = re.subn(r'(name=CAP_VALUES\b[^\n]*value=")',lambda m:m.group(1)+''.join(f'.param {k}={v}\n' for k,v in missing),text,count=1)
        assert count == 1, f'No visible CAP_VALUES block in {file}'
        file.write_text(text); filled.append({'schematic':str(file.relative_to(work)),'visible_defaults_added':dict(missing)})
# The same saved projects run with normal Xschem and a local rcfile; a global
# xschem-800nm launcher is not needed in a fresh clone.
f = work/'Integrated_Design/run_simulation.py'
s = f.read_text().replace("['xschem-800nm','-x','-q'", "['xschem','--rcfile',str(r/'xschemrc'),'-x','-q'")
f.write_text(s)
if args.runtime:
    runtime = args.runtime.expanduser().resolve()
    for name in ['bin/iverilog','bin/vvp','lib/libvvp.so','lib/ngspice/ivlng.so','lib/ngspice/ivlng.vpi']:
        assert (runtime/name).is_file(), f'Missing {runtime/name}'
    (work/'Phase_Generator_Testbench/runtime').symlink_to(runtime,target_is_directory=True)
(ROOT/'local_setup.json').write_text(json.dumps({'pdk_root':str(pdk),'work':str(work),'visible_defaults_added':filled,'runtime_reused':str(args.runtime) if args.runtime else None},indent=2))
print('Configured working copies:',work)
print('Edit capacitor values in work/Integrated_Design/schematic/ using Xschem.')
print('Setup record:', ROOT/'local_setup.json')
