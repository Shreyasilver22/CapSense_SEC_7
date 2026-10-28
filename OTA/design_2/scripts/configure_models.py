from pathlib import Path
import argparse
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('model_file',type=Path);a=p.parse_args();model=a.model_file.expanduser().resolve()
if not model.is_file():raise SystemExit('Model file does not exist')
if any(x in str(model) for x in ['"','\n','\r']):raise SystemExit('Unsupported path characters')
(root/'spice/models.inc').write_text('* Local private SCL nominal transistor models; not bundled.\n.include "'+str(model)+'"\n')
print('Configured local SCL models. No model cards copied.')
