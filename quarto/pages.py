"""Write one .qmd per template, plus the index that links them.

Generated rather than parameterised, which is the opposite of where this spike started.
Quarto does take `-P`, but with the Python engine it routes through papermill, and
papermill renders a copy of the file under a temporary name - so the page's title becomes
`quarto-inputa2d3288ac1e1f384`, the output file is `template.html` whichever template it
holds, and the website's search index has one entry called "template". A four-line stub
per template costs nothing and gives Quarto what it is built around: a file per page,
named after the page.

    uv run --group docs quarto/pages.py F_18.00.a K_47.00.a    # named templates
    uv run --group docs quarto/pages.py --framework DORA       # a whole framework
    uv run --group docs quarto/pages.py --framework COREP FINREP   # or several
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _dpm as dpm  # noqa: E402  - the path has to be set before this resolves

STUB = """---
title: {title}
---

```{{python}}
#| echo: false
table_code = "{code}"
db = {db}
```

{{{{< include _body.qmd >}}}}
"""

INDEX = """---
title: {title}
---

```{{python}}
#| echo: false
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import _dpm as dpm

con = dpm.connect({db})
known = dpm.releases(con)
templates = dpm.templates_of(con, "{framework}")
```

```{{python}}
#| echo: false
#| output: asis
print(
    f"{{len(templates)}} templates with reportable cells, read from a DPM database "
    f"carrying releases {{known[0]['code']}} to {{known[-1]['code']}}.\\n"
)
print(dpm.markdown_table(
    [
        {{"template": f"[{{row['table_code']}}]({{row['table_code']}}.html)", "name": row["name"]}}
        for row in templates
    ],
    ["template", "name"],
))
```
"""


def yaml_string(text: str) -> str:
    """A title as a YAML scalar that survives whatever is in it.

    json.dumps rather than quoting by hand: YAML 1.2 reads a JSON string, and a template
    name is not always a safe bare scalar - F_40.02 is "Scope of the group:
    \"instrument-by-instrument\"", which has both the colon and the quotes that end a
    title early. Quarto's answer to that is a YAMLException and no pages at all.
    """
    return json.dumps(text)


def stub(code: str, name: str, db: str | None) -> str:
    """The page for one template. The body is included, never copied."""
    return STUB.format(code=code, title=yaml_string(f"{code} - {name}"), db=repr(db or ""))


def index(framework: str, db: str | None) -> str:
    """The page that links a framework's templates, with their names."""
    return INDEX.format(framework=framework, title=yaml_string(framework), db=repr(db) if db else "None")


def write(codes: list[str], db: str | None = None) -> list[Path]:
    """Write a page per template, and return what was written.

    The name comes out of the database rather than from the caller: a title typed by hand
    is a title that disagrees with the model after the next release.
    """
    con = dpm.connect(db)
    written = []
    for code in codes:
        found = dpm.versions(con, code)
        if not found:
            raise SystemExit(f"{code} is not a template in this database.")
        page = HERE / f"{code}.qmd"
        page.write_text(stub(code, found[-1]["name"], db), encoding="utf-8")
        written.append(page)
    return written


def write_framework(framework: str, db: str | None = None) -> list[Path]:
    """Every template of one framework, and the index that lists them."""
    con = dpm.connect(db)
    found = dpm.templates_of(con, framework)
    if not found:
        raise SystemExit(f"{framework} is not a framework in this database, or has no reportable cells.")
    pages = write([row["table_code"] for row in found], db)
    listing = HERE / f"{framework}.qmd"
    listing.write_text(index(framework, db), encoding="utf-8")
    return [listing, *pages]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", nargs="*", help="template codes, e.g. F_18.00.a")
    parser.add_argument(
        "--framework",
        nargs="+",
        metavar="NAME",
        help="every template of these frameworks instead, e.g. --framework FINREP COREP",
    )
    parser.add_argument("--db", help="a DPM database other than the default")
    args = parser.parse_args()
    if not args.templates and not args.framework:
        parser.error("name some templates, or a --framework")
    written = (
        [page for framework in args.framework for page in write_framework(framework, args.db)]
        if args.framework
        else write(args.templates, args.db)
    )
    for path in written:
        print(path.name)
