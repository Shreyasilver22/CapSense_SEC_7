"""Create an ignored local model include; never copy PDK model cards into Git."""
from pathlib import Path
import argparse,os
p=argparse.ArgumentParser();p.add_argument('model_file',nargs='?',default=os.environ.get('SCL_MODEL_FILE'));a=p.parse_args()
if not a.model_file:p.error('Pass the local SCL tntp49_5v MOS model file or set SCL_MODEL_FILE.')
m=Path(a.model_file).expanduser().resolve()
if not m.is_file():p.error('Model file does not exist: '+str(m))
if '"' in str(m) or '\n' in str(m):p.error('Unsupported character in model path.')
out=Path(__file__).resolve().parents[1]/'spice/models.inc'
out.write_text('* Local-only PDK include. Ignored by Git.\n.include "'+str(m)+'"\n')
print('Configured local model include:',out)
