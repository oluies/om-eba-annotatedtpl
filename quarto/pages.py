"""Write one .qmd per template: a title, which template, and the shared body.

Generated rather than parameterised, which is the opposite of where this spike started.
Quarto does take `-P`, but with the Python engine it routes through papermill, and
papermill renders a copy of the file under a temporary name - so the page's title becomes
`quarto-inputa2d3288ac1e1f384`, the output file is `template.html` whichever template it
holds, and the website's search index has one entry called "template". A four-line stub
per template costs nothing and gives Quarto what it is built around: a file per page,
named after the page.

    uv run --group docs quarto/pages.py F_18.00.a K_47.00.a
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _dpm as dpm  # noqa: E402  - the path has to be set before this resolves

STUB = """---
title: "{title}"
---

```{{python}}
#| echo: false
table_code = "{code}"
db = ""
```

{{{{< include _body.qmd >}}}}
"""


def stub(code: str, name: str) -> str:
    """The page for one template. The body is included, never copied."""
    return STUB.format(code=code, title=f"{code} - {name}")


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
        page.write_text(stub(code, found[-1]["name"]), encoding="utf-8")
        written.append(page)
    return written


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: pages.py <TEMPLATE_CODE>...")
    for path in write(sys.argv[1:]):
        print(path.name)
