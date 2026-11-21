"""Build a comparison gain-boosted macro with the project's SCL08 layout template."""
from pathlib import Path
import json
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
MIRROR = ROOT / 'fixtures'
TEMPLATE = MIRROR / 'cmfb_revision_20261101/scripts/generate.py'
TECH = Path.home()/'pdk/scl08/analog_pdk/Open_Source_SCL_0.8micron_PDK/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/klayout/tech'
WORK = ROOT/'boosted_layout'


def prepare():
    for name in ('scripts','models','schematic','layout','verification'):
        (WORK/name).mkdir(exist_ok=True,parents=True)
    s = TEMPLATE.read_text()
    replacements = {
        'ota_telescopic_layout': 'ota_boosted_layout',
        ",'VBN','VBP']": ",'NBOOST','PBOOST']",
        "'nb':'VBN','pb':'VBP'": "'vr':'NBOOST','vrp':'PBOOST'",
        'source_telescopic.spice': 'source_boosted.spice',
        'segments=40': 'segments=160',
    }
    for old,new in replacements.items():
        if old not in s:
            raise ValueError(f'Layout template change: {old!r}')
        s = s.replace(old,new)
    (WORK/'scripts/generate.py').write_text(s)
    (WORK/'selected.json').write_text(json.dumps({'R_kohm': 1000}))
    (WORK/'models/source_boosted.spice').write_text((ROOT/'models/boosted.spice').read_text())


def check(gds, reference, out):
    result = {}
    for kind, rule, params in (
        ('drc', 'drc/cp8d_drc.drc', {'report1':out/'drc.lyrdb'}),
        ('lvs', 'lvs/lvs_os_scl_cp8d.lvs', {'schematic1':reference,
                'target_netlist1':out/'extracted.cir','report':out/'lvs.lvsdb'}),
    ):
        args = ['klayout','-b','-r',str(TECH/rule),'-rd',f'input={gds}']
        for key,val in params.items():
            args += ['-rd',f'{key}={val}']
        p = subprocess.run(args,capture_output=True,text=True,timeout=180)
        log = p.stdout + p.stderr
        (out/f'{kind}.log').write_text(log)
        p.check_returncode()
        if kind == 'drc':
            result['DRC_markers'] = len(ET.parse(out/'drc.lyrdb').findall('.//items/item'))
        else:
            result['LVS_match'] = 'INFO : Congratulations! Netlists match.' in log
    (out/'check.json').write_text(json.dumps(result,indent=2))
    return result


def main():
    prepare()
    subprocess.run(['klayout','-b','-r',str(WORK/'scripts/generate.py')],check=True,timeout=180)
    a = check(WORK/'layout/ota_boosted_layout.gds',WORK/'schematic/reference.cdl',WORK/'verification')
    print('Gain boosted',a,flush=True)
    tel = ROOT.parent/'architecture_exploration_20261031/cmfb_revision_20261101'
    reference = MIRROR/'cmfb_revision_20261101/schematic/reference.cdl'
    gds = ROOT.parent.parent/'layout/ota_telescopic_layout.gds'
    out = ROOT/'telescopic_layout_check'
    out.mkdir(exist_ok=True)
    b = check(gds,reference,out)
    print('Telescopic',b,flush=True)

if __name__ == '__main__':
    main()

