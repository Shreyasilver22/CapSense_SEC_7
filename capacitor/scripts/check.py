from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
for name in ['symbols.py','examples.py','make_prepare_fixture.py','verify.py','report.py']:
 subprocess.run([sys.executable,str(root/'scripts'/name)],check=True,cwd=root)
print('Capacitor model/symbol/example checks passed; physical extraction remains experimental.')
