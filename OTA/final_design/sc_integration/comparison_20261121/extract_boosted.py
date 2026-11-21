from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'boosted_layout'
SOURCE = ROOT / 'fixtures/cmfb_revision_20261101/scripts'


def main():
    (WORK/'pex').mkdir(exist_ok=True)
    place = (SOURCE/'extract.py').read_text().replace('ota_telescopic_layout','ota_boosted_layout')
    if not Path('/tmp/magic_ota_tool/bin/magic').exists():
        place = place.replace('/tmp/magic_ota_tool/bin/magic',shutil.which('magic'))
    (WORK/'scripts/extract.py').write_text(place)
    subprocess.run(['python3',str(WORK/'scripts/extract.py')],check=True)
    export = (SOURCE/'export_models.py').read_text()
    lo = export.index('# Matching pre-layout macro:')
    hi = export.index('caps={',lo)
    export = (export[:lo]+export[hi:]).replace('ota_telescopic_layout','ota_boosted_layout')
    export = export.replace('assert len(dev)==80','assert len(dev)==320')
    (WORK/'scripts/export_models.py').write_text(export)
    subprocess.run(['python3',str(WORK/'scripts/export_models.py')],check=True)
    for line in (WORK/'models/layout_C.spice').read_text().splitlines():
        if line.lower().startswith('.subckt'):
            print(line)
    shutil.copyfile(WORK/'models/layout_C.spice',ROOT/'models/boosted_C.spice')


if __name__ == '__main__':
    main()

