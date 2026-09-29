"""Normalise the EBA PAY 4.2 annotated table layout into datapoints + dimensions."""

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

import openpyxl

# Paths resolve against the repository root so the pipeline reproduces from a fresh
# clone: `uv run source/extract_dpm.py && uv run source/vocab.py && uv run source/gen_pack.py`.
REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "source"
XLSX = SOURCE / "20260106_Annotated_Table_Layout__PAY_4.2_PSD_FRPPAY_4.2.xlsx"
DPM_JSON = SOURCE / "dpm.json"
VOCAB_JSON = SOURCE / "vocab.json"


DIM_RE = re.compile(r"^\((?P<owner>[A-Za-z0-9]+):(?P<code>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")
PROP_RE = re.compile(r"^\((?P<code>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")


def clean(v: Any) -> str:
    if v is None:
        return ""
    s = str(v).replace("_x000D_", "").replace("\r", "\n")
    s = unicodedata.normalize("NFKC", s)
    return "\n".join(line.strip() for line in s.split("\n")).strip()


def parse_dim(text: str) -> dict[str, str] | None:
    """'(qEEB:qET) Event Type' -> {'dim': 'qEEB', 'axis': 'qET', 'label': 'Event Type'}"""
    m = DIM_RE.match(text)
    if m:
        return {"dim": m["owner"], "member": m["code"], "label": m["label"]}
    m = PROP_RE.match(text)
    if m:
        return {"dim": m["code"], "member": "", "label": m["label"]}
    return None


def build_grid(ws) -> tuple[dict, dict]:
    """Cell values plus a map of merged coordinates to their anchor value."""
    merged = {}
    spans = {}
    for rng in ws.merged_cells.ranges:
        anchor = clean(ws.cell(rng.min_row, rng.min_col).value)
        spans[(rng.min_row, rng.min_col)] = (rng.min_col, rng.max_col, rng.min_row, rng.max_row)
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                merged[(r, c)] = anchor
    cells = {}
    for row in ws.iter_rows():
        for cell in row:
            v = clean(cell.value)
            if v:
                cells[(cell.row, cell.column)] = v
    return cells, spans


def find(cells, text):
    return next((rc for rc, v in cells.items() if v == text), None)


def parse_sheet(ws) -> dict:
    cells, spans = build_grid(ws)
    title = cells.get((1, 1), ws.title)

    col_rc = find(cells, "Columns")
    row_rc = find(cells, "Rows")
    if not col_rc or not row_rc:
        return {}

    col_row, col_col = col_rc
    dmin, dmax = spans.get(col_rc, (col_col, col_col, 0, 0))[:2]
    data_cols = list(range(dmin, dmax + 1))
    label_row, code_row = col_row + 1, col_row + 2

    # Dimension NAME columns sit to the right of the data block on the "Columns" row.
    dim_cols = {c: parse_dim(cells[(col_row, c)]) for c in range(dmax + 1, ws.max_column + 1) if (col_row, c) in cells}
    dim_cols = {c: d for c, d in dim_cols.items() if d}

    rmin_row, rmax_row = spans.get(row_rc, (0, 0, row_rc[0], row_rc[0]))[2:]

    columns = [
        {"code": cells.get((code_row, c), ""), "label": cells.get((label_row, c), ""), "_col": c} for c in data_cols
    ]

    # Footer: dimension name in col B, member per data column. These are the column-axis
    # members, plus the table-level main property.
    footer = []
    for r in range(rmax_row + 1, ws.max_row + 1):
        name = cells.get((r, 2), "")
        if not name:
            continue
        entry = {"name": name, "dim": parse_dim(name), "per_column": {}}
        for c in data_cols:
            v = cells.get((r, c), "")
            if v:
                entry["per_column"][cells.get((code_row, c), str(c))] = v
        footer.append(entry)

    # Header z-axis. "Main Property" anchors it: when that label sits ABOVE the Columns
    # row the block is two rows (names, then members); when it sits below the Rows block
    # it is a footer row instead and the footer parser above already has it.
    mp_rc = find(cells, "Main Property")
    z_axis = []
    main_property = ""
    sheet_label = ""
    if mp_rc and mp_rc[0] < col_row:
        name_row = mp_rc[0]
        value_row = name_row + 1
        for c in range(dmax + 1, ws.max_column + 1):
            name, member = cells.get((name_row, c), ""), cells.get((value_row, c), "")
            if name and member:
                z_axis.append({"name": name, "member": member, "dim": parse_dim(member)})
        main_property = cells.get((value_row, dmin), "")
        sheet_label = cells.get((value_row, 2), "")

    rows = []
    for r in range(rmin_row, rmax_row + 1):
        label, code = cells.get((r, 2), ""), cells.get((r, 3), "")
        if not label:
            continue
        # Which column a member sits in is what identifies its dimension: the member cell
        # itself only carries the DOMAIN code, which several dimensions share.
        members = []
        for c, dim_header in dim_cols.items():
            if (r, c) not in cells:
                continue
            m = parse_dim(cells[(r, c)])
            if m:
                members.append(m | {"dimension": dim_header["label"], "dimension_code": dim_header["dim"]})
        datapoints = {}
        for c in data_cols:
            raw = cells.get((r, c), "")
            if not raw:
                continue
            parts = [p for p in raw.split("\n") if p]
            if parts and parts[0].isdigit():
                datapoints[cells.get((code_row, c), str(c))] = {
                    "id": parts[0],
                    "unit": parts[1] if len(parts) > 1 else "",
                    "sign": parts[2] if len(parts) > 2 else "",
                }
        rows.append(
            {
                "code": code,
                "label": label,
                "is_header": not code and not datapoints,
                "members": members,
                "datapoints": datapoints,
            }
        )

    return {
        "sheet": ws.title,
        "title": title,
        "sheet_label": sheet_label,
        "main_property": main_property,
        "z_axis": z_axis,
        "columns": columns,
        "column_dimension_names": {str(c): d for c, d in dim_cols.items()},
        "footer": footer,
        "rows": rows,
    }


wb = openpyxl.load_workbook(XLSX, data_only=True)
toc = {}
for row in wb["TOC"].iter_rows(min_row=3):
    code, label = clean(row[1].value), clean(row[2].value)
    if code:
        toc.setdefault(code, label)

sheets = [parse_sheet(wb[n]) for n in wb.sheetnames if n != "TOC"]
sheets = [s for s in sheets if s]
DPM_JSON.write_text(json.dumps({"toc": toc, "sheets": sheets}, ensure_ascii=False, indent=1), encoding="utf-8")

n_dp = sum(len(r["datapoints"]) for s in sheets for r in s["rows"])
print(f"sheets parsed: {len(sheets)} / {len(wb.sheetnames) - 1}")
print(f"datapoints:    {n_dp}")
print(f"TOC entries:   {len(toc)}")
