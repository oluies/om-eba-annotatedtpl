import json
import re
from collections import defaultdict
from pathlib import Path

# Paths resolve against the repository root so the pipeline reproduces from a fresh
# clone: `uv run source/extract_dpm.py && uv run source/vocab.py && uv run source/gen_pack.py`.
REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "source"
XLSX = SOURCE / "20260106_Annotated_Table_Layout__PAY_4.2_PSD_FRPPAY_4.2.xlsx"
DPM_JSON = SOURCE / "dpm.json"
VOCAB_JSON = SOURCE / "vocab.json"


PAIR = re.compile(r"^\((?P<a>[A-Za-z0-9]+):(?P<b>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")
SOLO = re.compile(r"^\((?P<a>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")

data = json.loads(DPM_JSON.read_text(encoding="utf-8"))

dimensions: dict[str, dict] = {}  # dim code -> {label, domain}
domains: dict[str, dict[str, str]] = defaultdict(dict)  # domain -> {member: label}
properties: dict[str, str] = {}  # metric/main property code -> label


def add_dimension(text: str) -> None:
    m = PAIR.match(text or "")
    if m:
        dimensions[m["a"]] = {"label": m["label"], "domain": m["b"]}


def add_member(text: str) -> None:
    m = PAIR.match(text or "")
    if m:
        domains[m["a"]][m["b"]] = m["label"]


def add_property(text: str) -> None:
    m = SOLO.match(text or "")
    if m:
        properties[m["a"]] = m["label"]


for s in data["sheets"]:
    add_property(s["main_property"])
    for d in s["column_dimension_names"].values():
        add_dimension(f"({d['dim']}:{d['member']}) {d['label']}")
    for z in s["z_axis"]:
        add_dimension(z["name"])
        add_member(z["member"])
    for f in s["footer"]:
        add_dimension(f["name"])
        add_property(f["name"])
        for v in f["per_column"].values():
            add_member(v)
            add_property(v)
    for r in s["rows"]:
        for m in r["members"]:
            if m.get("member"):
                add_member(f"({m['dim']}:{m['member']}) {m['label']}")

VOCAB_JSON.write_text(
    json.dumps({"dimensions": dimensions, "domains": domains, "properties": properties}, ensure_ascii=False, indent=1),
    encoding="utf-8",
)

print(f"dimensions: {len(dimensions)}   domains: {len(domains)}   properties: {len(properties)}")
print("\n--- dimensions ---")
for code, d in sorted(dimensions.items(), key=lambda kv: (kv[1]["domain"], kv[1]["label"])):
    print(f"  {code:6} domain={d['domain']:4} {d['label']}")
print("\n--- domains ---")
for dom, mem in sorted(domains.items()):
    print(f"  {dom:5} {len(mem):3} members")
print("\n--- properties (metrics) ---")
for code, label in sorted(properties.items()):
    print(f"  {code:8} {label}")
