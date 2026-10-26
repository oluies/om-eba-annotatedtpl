"""Which templates get a page, and what they are called, from the DPM.

A data loader: Observable runs it at build and keeps the output. The list is read by
observablehq.config.js to decide which pages exist, so a template withdrawn upstream
stops having a page without anyone deleting a file - which is what the generated-stub
approach this replaces could not do.
"""

import json
import os
import sys
from pathlib import Path

# The query layer is shared with the Quarto pages rather than written twice. It still
# lives under quarto/ because that is where it was first needed; that is a name to fix,
# not a second copy to make.
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "quarto"))

import _dpm as dpm  # noqa: E402

FRAMEWORKS = os.environ.get("OBS_FRAMEWORKS", "COREP FINREP").split()

con = dpm.connect(os.environ.get("DPM2_DB") or None)
seen: dict[str, str] = {}
for framework in FRAMEWORKS:
    for row in dpm.templates_of(con, framework):
        seen.setdefault(row["table_code"], row["name"])
json.dump([{"code": code, "name": name} for code, name in sorted(seen.items())], sys.stdout)
