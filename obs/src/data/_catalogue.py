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

# Shared with the markdown Quarto writes for the catalogue rather than written twice: a
# number must not mean one thing on a page and another in the article about it.
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "source"))

import dpm_pages as dpm  # noqa: E402

FRAMEWORKS = os.environ.get("OBS_FRAMEWORKS", "COREP FINREP").split()

# Which releases the publish writes. A template withdrawn before the oldest of them has a
# page a reader cannot get an answer out of under any release the selector offers, so it
# is not listed. Empty means every release the database carries, which is what a local
# build against one database wants.
RELEASES = os.environ.get("OBS_RELEASES", "").split()

con = dpm.connect(os.environ.get("DPM2_DB") or None)

# The framework and the modules go with the template, not only its name. A page asked
# under the wrong framework can only answer "no reportable cells" - and no template of the
# 312 is in two frameworks, so that choice was a control whose every other setting was
# wrong. The modules are what the index groups by: own funds, leverage, large exposures,
# LCR and NSFR are separate submissions, and a run of 312 codes is not navigable.
found = [(framework, row) for framework in FRAMEWORKS for row in dpm.templates_of(con, framework, RELEASES)]
of_code = {
    code: [row for framework, row in found if row["table_code"] == code]
    for code in {row["table_code"] for _, row in found}
}

json.dump(
    [
        {
            "code": code,
            "name": of_code[code][0]["name"],
            "frameworks": sorted({framework for framework, row in found if row["table_code"] == code}),
            "modules": sorted({module for row in of_code[code] for module in (row["modules"] or "").split()}),
            # What the reporter adds rather than fills in. 14 of DORA's 15 templates and
            # 66 of COREP's 159 are open, and on those the cell count is the shape of one
            # row rather than the size of the submission.
            "open": [
                what for what in ("rows", "columns", "sheets") if any(row[f"open_{what}"] for row in of_code[code])
            ],
        }
        for code in sorted(of_code)
    ],
    sys.stdout,
)
