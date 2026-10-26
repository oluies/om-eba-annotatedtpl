```js
const code = observable.params.code;
const catalogue = await FileAttachment("../data/catalogue.json").json();
const name = (catalogue.find((d) => d.code === code) || {}).name ?? "";
const published = await FileAttachment("../data/releases.json").json();
```

```js
import {DuckDBClient} from "npm:@observablehq/duckdb";

// Read over HTTP from the tree the publish already writes, rather than attached as
// files. Three reasons, and the first is the one that bit: our partitioned parquet names
// every partition `data_0.parquet`, and Observable's attachment handling collides on the
// basename, so `cells` came back as the three columns it shares with `cell_members`.
// Reading a URL has no such naming. It also keeps one copy of the data for both this and
// the query page, and it is what makes the release selector work at all - a different
// release is a different URL, not a different build.
const db = await DuckDBClient.of();
// Two levels up from /<site>/templates/t/<code> is /<site>/, where the publish puts the
// parquet - and resolving against the document rather than against import.meta.url keeps
// that true wherever the site is mounted, which on Pages is a project path and not a root.
const base = new URL("../../data/", document.baseURI).href;
const at = (release, path) => `${base}${release}/${path}`;
```

```js
const release = view(Inputs.select(published, {
  label: "DPM release",
  value: published.at(-1),
  // Newest last in the file; newest first in the list, because that is what is asked for.
  format: (d) => d,
}));
```

```js
const framework = view(Inputs.select(["FINREP", "COREP"], {label: "Framework", value: code.startsWith("F_") ? "FINREP" : "COREP"}));
```

```js
// One query per section, re-run when the release changes. This is the thing a rendered
// document cannot do: the page is not three releases deep, it asks again.
const grid = await db.query(`
  SELECT DISTINCT row_code, row_label, column_code, column_label, datapoint,
         '{' || table_code || ', r' || row_code || ', c' || column_code || '}' AS cell
  FROM '${at(release, `cells/framework=${framework}/data_0.parquet`)}'
  WHERE table_code = '${code}' ORDER BY row_code, column_code`);

const dimensions = await db.query(`
  SELECT dimension, count(DISTINCT member) AS members,
         string_agg(DISTINCT member, ', ' ORDER BY member) AS wording
  FROM '${at(release, `cell_members/framework=${framework}/data_0.parquet`)}'
  WHERE table_code = '${code}' GROUP BY dimension ORDER BY dimension`);

const checks = await db.query(`
  WITH here AS (SELECT DISTINCT operation_vid
                FROM '${at(release, `rule_cells/framework=${framework}/data_0.parquet`)}'
                WHERE table_code = '${code}')
  SELECT DISTINCT r.rule_code, r.severity, r.active, r.module, r.taxonomy_version
  FROM '${at(release, "rules.parquet")}' r JOIN here USING (operation_vid)
  ORDER BY r.rule_code`);
```

# ${code} — ${name}

```js
const off = checks.toArray().filter((d) => !d.active).length;
const nothing = grid.numRows === 0;
```

```js
display(html`<p>${nothing
  ? html`<em>${code} has no reportable cells in DPM ${release} under ${framework}. A template is
      introduced and withdrawn; try another release, or the other framework.</em>`
  : html`<strong>${grid.numRows.toLocaleString("sv")} reportable cells</strong>,
      ${dimensions.numRows} dimensions, ${checks.numRows} validation rules reaching it,
      ${off} of them switched off — in DPM ${release}. These numbers are the query's
      answer, asked again when you change the release above.`}</p>`);
```

## Every cell

```js
const found = view(Inputs.search(grid, {placeholder: "a row label, a code, anything…"}));
```

```js
Inputs.table(found, {
  columns: ["row_code", "row_label", "column_code", "column_label", "cell", "datapoint"],
  header: {row_code: "row", row_label: "row label", column_code: "col", column_label: "column label"},
  rows: 16,
})
```

## What it breaks down by

The members are in the model's own wording, which is the wording a query has to match: a
near miss matches nothing rather than erroring, and a trailing space is a real difference.

```js
Inputs.table(dimensions, {columns: ["dimension", "members", "wording"], rows: 8})
```

## What checks it

`active` is the EBA's deactivated-rules list. A description telling a reader to satisfy a
rule nobody runs is worse than one naming none. A code is not a stable statement either —
2 005 of 7 514 consecutive versions of a rule change the expression — so each links to
what it checks under this release.

```js
const whichRules = view(Inputs.search(checks, {placeholder: "a rule code, a severity, a module…"}));
```

```js
Inputs.table(whichRules, {
  rows: 12,
  format: {
    rule_code: (d) => html`<a href="https://oluies.github.io/om-eba-annotatedtpl/?q=rule&rule_code=${d}&release=${release}">${d}</a>`,
  },
})
```
