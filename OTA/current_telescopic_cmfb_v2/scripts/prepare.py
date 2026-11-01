"""Regenerate the chosen source model; leaves rejected screening results intact."""
import json
import sweep as s
p=json.loads((s.R/'selected.json').read_text())
(s.R/'models/source_telescopic.spice').write_text(s.source(p,False))
print(s.key(p))
