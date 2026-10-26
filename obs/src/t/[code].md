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

// A partition that holds nothing is not written at all - no FINREP template has a
// reworded row, so there is no relabelled/framework=FINREP/ - and DuckDB answers a
// missing file by throwing, which killed every cell on the page rather than the one
// section. An absent table is an empty table here.
const maybe = async (sql) => {
  try {
    return await db.query(sql);
  } catch (problem) {
    return {numRows: 0, toArray: () => [], get: () => undefined};
  }
};
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

const dimensions = await maybe(`
  SELECT dimension, count(DISTINCT member) AS members,
         string_agg(DISTINCT member, ', ' ORDER BY member) AS wording
  FROM '${at(release, `cell_members/framework=${framework}/data_0.parquet`)}'
  WHERE table_code = '${code}' GROUP BY dimension ORDER BY dimension`);

// The regulation's own wording, which is not a translation: the templates are an annex to
// an Implementing Regulation and one is published in all 24 official languages. Not
// release-scoped the way everything above is - a regulation has its own versions, and the
// `celex` column says which text a row came from.
const wording = await maybe(`
  SELECT row, en, sv, de, celex, "from"
  FROM '${base}its_labels.csv'
  WHERE template = '${code}' ORDER BY row`);

const spelled = await maybe(`
  SELECT row, en, sv, celex
  FROM '${base}its_instructions.csv'
  WHERE template = '${code}' ORDER BY row`);

const reworded = await maybe(`
  SELECT row, celex, en
  FROM '${base}its_label_changes.csv'
  WHERE template = '${code}' ORDER BY row, celex`);

// What has changed is the one thing on this page that is not an answer under the chosen
// release: it is a comparison across all of them, so the publish precomputes it.
const drift = await maybe(`
  SELECT datapoints, moved, shared
  FROM '${at(release, `template_changes/framework=${framework}/data_0.parquet`)}'
  WHERE table_code = '${code}'`);

// Ordered by header and not by row code: a template can serve one code from two
// headers, and reading them as one row makes a pair of unrelated labels look like a
// rewording. The row is the header.
const reworded_rows = await maybe(`
  SELECT row_code, from_release, to_release, label
  FROM '${at(release, `relabelled/framework=${framework}/data_0.parquet`)}'
  WHERE table_code = '${code}' ORDER BY row_code, header_id, start_release_id`);

const checks = await maybe(`
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

## The same rows in Swedish and German

```js
display(wording.numRows === 0
  ? html`<p><em>No published wording for ${code}. The regulation that carries these
      translations is the supervisory reporting ITS; DORA, MiCA and remuneration are
      separate regulations, not yet read.</em></p>`
  : html`<p>Not a translation. ${wording.numRows} of this template's rows have a wording
      published in every official language, from
      <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:${wording.get(0).celex}">${wording.get(0).celex}</a>,
      the consolidated regulation. <code>from</code> says <code>stem</code> where the
      Journal printed that grid once, under the template this one varies.</p>`);
```

```js
const inSwedish = view(Inputs.search(wording, {placeholder: "a row, or a word in any of the three…"}));
```

```js
Inputs.table(inSwedish, {
  columns: ["row", "en", "sv", "de", "from"],
  header: {en: "English", sv: "Svenska", de: "Deutsch"},
  rows: 14,
})
```

```js
// An empty html template literal evaluates to null, and display(null) writes the word
// "null" onto the page. Nothing is displayed by not calling display.
if (reworded.numRows > 0) display(html`<h3>Rows the regulation has reworded</h3>
  <p>The datapoint did not change and neither did the cell. The sentence did.</p>
  ${Inputs.table(reworded, {columns: ["row", "celex", "en"], rows: 8})}`);
```

## What the regulation says these rows are

```js
display(spelled.numRows === 0
  ? html`<p><em>The instructions annex says nothing about ${code}'s rows in particular.
      COREP's is a table of row code and prose and gives 1 040 of these; FINREP's Annex V
      is narrative guidance naming an item by quoting its label, which attaches to a row
      only 37 times. Most of its 708 paragraphs are about accounting treatment and belong
      to no row.</em></p>`
  : html`<p>${spelled.numRows} rows have a meaning and an article given in the
      instructions annex — in Swedish too.</p>`);
```

```js
const defined = view(Inputs.search(spelled, {placeholder: "a row, an article, a word…"}));
```

```js
Inputs.table(defined, {
  columns: ["row", "en", "sv"],
  header: {en: "What the regulation says", sv: "Vad förordningen säger"},
  rows: 8,
  width: {en: 420, sv: 420},
})
```

## What it breaks down by

The members are in the model's own wording, which is the wording a query has to match: a
near miss matches nothing rather than erroring, and a trailing space is a real difference.

```js
Inputs.table(dimensions, {columns: ["dimension", "members", "wording"], rows: 8})
```

## What has changed

The EBA ships no account of this — the DPM's `ChangeLog` table is present and empty in
every release — so it is read off the version rows.

```js
display(drift.numRows === 0
  ? html`<p><em>No comparison for ${code} under ${framework}.</em></p>`
  : html`<p>Of the ${drift.get(0).datapoints.toLocaleString("sv")} datapoints this template
      reports, <strong>${drift.get(0).moved.toLocaleString("sv")} have sat at another row or
      column</strong> at some point. The datapoint is the thing that persisted; the
      coordinate is where it happened to be that release — which is why a time series keyed
      on the coordinate is keyed on an address. A further
      ${drift.get(0).shared.toLocaleString("sv")} are reported by more than one template,
      which is the layout and not a change: the variants of a template share datapoints.</p>`);
```

```js
display(reworded_rows.numRows === 0
  ? html`<p>No row of this template has been reworded since it was introduced.</p>`
  : html`<h3>Rows the EBA has reworded</h3>
      <p>The coordinate stayed, the datapoint stayed, the sentence shown to a reader did
      not — which is the change nobody notices, because nothing in a report looks
      different.</p>
      ${Inputs.table(reworded_rows, {columns: ["row_code", "from_release", "to_release", "label"],
                                     header: {row_code: "row"}, rows: 10})}`);
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
