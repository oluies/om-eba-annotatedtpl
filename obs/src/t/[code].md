```js
const code = observable.params.code;
const catalogue = await FileAttachment("../data/catalogue.json").json();
const listed = catalogue.find((d) => d.code === code) || {};
const name = listed.name ?? "";
const published = await FileAttachment("../data/releases.json").json();

// Which framework files this template, from the catalogue rather than from the reader.
// No template of the 312 belongs to two, so a free choice was a control whose every
// setting but one produced "no reportable cells in DPM x" - an empty page that reads like
// a fault. It stays a list in case a publish ever holds one that is in two.
const belongs = listed.frameworks?.length ? listed.frameworks : [code.startsWith("F_") ? "FINREP" : "COREP"];

// What the reporter adds rather than fills in. On a closed template the cell count is the
// whole thing; on an open one it is the shape of a row, and the number of rows is however
// many contracts, entities or exposures there are. Every DORA register template is open.
const openness = listed.open ?? [];
```

```js
// Two levels up from /<site>/templates/t/<code> is /<site>/, where the publish puts the
// parquet - and resolving against the document rather than against import.meta.url keeps
// that true wherever the site is mounted, which on Pages is a project path and not a root.
// `?data=` points the page at another published tree, which is how it is driven against
// the published data from a local preview.
//
// In its own cell because the cell that fetches must not name the one that holds the
// engine: two cells that reference each other are a circular definition, and Observable
// answers that by failing every cell on the page.
const base = new URL(new URLSearchParams(location.search).get("data") ?? "../../data/", document.baseURI).href;
const at = (release, path) => `${base}${release}/${path}`;

// The regulation's own wording is not release-scoped - a regulation has its own versions,
// and every row carries the CELEX it came from - so it sits at the root rather than under
// a release, partitioned by framework like everything else.
const wordingOf = (name, framework) => `${base}${name}/framework=${framework}/data_0.parquet`;

// DuckDB picks its reader from the extension, so the name keeps it.
const named = (url) => url.replace(/^https?:\/\//, "").replace(/[^\w.]+/g, "_");
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

// Every file is fetched once and handed to DuckDB as bytes, rather than letting DuckDB read
// it over HTTP. Pages serves these gzipped, and then the content-length it reports is the
// compressed length while a byte range comes from the uncompressed file: DuckDB reads the
// footer where it was told the end is, finds no magic bytes there, and the section dies
// with "No magic bytes found at end of file". Which of the two variants the CDN holds
// decides whether a page works - that is how the FINREP pages failed while the COREP ones
// passed on the same code. fetch() decompresses, so the bytes are the file.
// Fetching is one half and registering is the other, and only the second needs the
// engine. Measured on a cold cache: 1.8 s passes before the first byte of data is asked
// for, because DuckDB-WASM is 8 MB and everything waited for it - and then the files were
// fetched one after another because each query awaited the one before. Both halves of
// that are avoidable: `arriving` starts every fetch as soon as the URLs are known, which
// is before the engine exists, and they run together.
const loaded = new Map();
const bytes = async (url) => {
  if (!loaded.has(url)) {
    loaded.set(url, (async () => {
      const buffer = await arriving(url);
      await db._db.registerFileBuffer(named(url), new Uint8Array(buffer));
      return named(url);
    })());
  }
  return loaded.get(url);
};

// Inputs.table and Inputs.search want something iterable, and an object carrying a numRows
// is not one: "TypeError: e is not iterable" is what the reader saw where a table should
// have been. An empty array with the two accessors the page uses answers both.
const absent = () => Object.assign([], {numRows: 0, get: () => undefined, toArray: () => []});

// A partition that holds nothing is not written at all - no FINREP template has a reworded
// row, so there is no relabelled/framework=FINREP/ - and a missing file is a throw, which
// killed every cell on the page rather than the one section. An absent table is an empty
// table here. `sql` is handed the registered name of each file it was given, in order.
const maybe = async (urls, sql) => {
  try {
    return await db.query(sql(...(await Promise.all(urls.map(bytes)))));
  } catch (problem) {
    return absent();
  }
};
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
// A select only where there is something to select.
const framework = belongs.length > 1
  ? view(Inputs.select(belongs, {label: "Framework", value: belongs[0]}))
  : belongs[0];
```

```js
// Every file this page reads, named in one place so that the fetching and the queries
// cannot drift apart.
const reads = [
  at(release, `cells/framework=${framework}/data_0.parquet`),
  at(release, `cell_members/framework=${framework}/data_0.parquet`),
  at(release, `template_changes/framework=${framework}/data_0.parquet`),
  at(release, `relabelled/framework=${framework}/data_0.parquet`),
  at(release, `rule_cells/framework=${framework}/data_0.parquet`),
  at(release, "rules.parquet"),
  wordingOf("its_labels", framework),
  wordingOf("its_instructions", framework),
  wordingOf("its_label_changes", framework),
];

// The four numbers the page opens with, precomputed by the publish from the same
// statements the queries below use. This is the one read whose answer is wanted before
// DuckDB-WASM exists - 360 ms to instantiate, 144 for the queries - so it is fetched as
// JSON and read by hand rather than through the engine.
const headline = fetch(at(release, `counts/${framework}.json`))
  .then((answer) => (answer.ok ? answer.json() : {}))
  .catch(() => ({}));

// This cell names no engine, so Framework runs it while DuckDB-WASM is still arriving.
// The relabelled partition is absent for a framework with no reworded row, and a fetch
// that rejects with nobody waiting is an unhandled rejection in the console - so each is
// marked handled here, and the rejection is still there for whoever awaits it.
const inFlight = new Map(reads.map((url) => {
  const started = fetch(url).then((answer) =>
    answer.ok ? answer.arrayBuffer() : Promise.reject(new Error(`${answer.status} ${answer.statusText} for ${url}`)));
  started.catch(() => {});
  return [url, started];
}));

const arriving = (url) => inFlight.get(url) ?? fetch(url).then((answer) => answer.arrayBuffer());
```

```js
// One query per section, re-run when the release changes. This is the thing a rendered
// document cannot do: the page is not three releases deep, it asks again.
const cells = await bytes(at(release, `cells/framework=${framework}/data_0.parquet`));
const grid = await db.query(`
  SELECT DISTINCT row_code, row_label, column_code, column_label, datapoint,
         '{' || table_code || ', r' || row_code || ', c' || column_code || '}' AS cell
  FROM '${cells}'
  WHERE table_code = '${code}' ORDER BY row_code, column_code`);

const dimensions = await maybe(
  [at(release, `cell_members/framework=${framework}/data_0.parquet`)],
  (members) => `
    SELECT dimension, count(DISTINCT member) AS members,
           string_agg(DISTINCT member, ', ' ORDER BY member) AS wording
    FROM '${members}'
    WHERE table_code = '${code}' GROUP BY dimension ORDER BY dimension`);

// The regulation's own wording, which is not a translation: the templates are an annex to
// an Implementing Regulation and one is published in all 24 official languages. Not
// release-scoped the way everything above is - a regulation has its own versions, and the
// `celex` column says which text a row came from.
const wording = await maybe([wordingOf("its_labels", framework)], (labels) => `
  SELECT row, en, sv, de, celex, "from"
  FROM '${labels}'
  WHERE template = '${code}' ORDER BY row`);

const spelled = await maybe([wordingOf("its_instructions", framework)], (instructions) => `
  SELECT row, en, sv, celex
  FROM '${instructions}'
  WHERE template = '${code}' ORDER BY row`);

const reworded = await maybe([wordingOf("its_label_changes", framework)], (changes) => `
  SELECT row, celex, en
  FROM '${changes}'
  WHERE template = '${code}' ORDER BY row, celex`);

// What has changed is the one thing on this page that is not an answer under the chosen
// release: it is a comparison across all of them, so the publish precomputes it.
const drift = await maybe(
  [at(release, `template_changes/framework=${framework}/data_0.parquet`)],
  (changes) => `
    SELECT datapoints, moved, shared
    FROM '${changes}'
    WHERE table_code = '${code}'`);

// Ordered by header and not by row code: a template can serve one code from two
// headers, and reading them as one row makes a pair of unrelated labels look like a
// rewording. The row is the header.
const reworded_rows = await maybe(
  [at(release, `relabelled/framework=${framework}/data_0.parquet`)],
  (relabelled) => `
    SELECT row_code, from_release, to_release, label
    FROM '${relabelled}'
    WHERE table_code = '${code}' ORDER BY row_code, header_id, start_release_id`);

const checks = await maybe(
  [at(release, `rule_cells/framework=${framework}/data_0.parquet`), at(release, "rules.parquet")],
  (reaching, rules) => `
    WITH here AS (SELECT DISTINCT operation_vid FROM '${reaching}' WHERE table_code = '${code}')
    SELECT DISTINCT r.rule_code, r.severity, r.active, r.module, r.taxonomy_version
    FROM '${rules}' r JOIN here USING (operation_vid)
    ORDER BY r.rule_code`);
```

# ${code} — ${name}

```js
// Four numbers rather than a sentence of four numbers: this is what the page answers, and
// a reader scanning for it should not have to read a paragraph to find it. `.card`, `.big`
// and the grid are the theme's own, so they follow light and dark without being told.
//
// Read from the precomputed file and not from the queries, so the page answers before the
// engine arrives. They are the same numbers: the publish computes them from the same
// statements, which is what keeps one fact from becoming two that disagree while the
// tables are still loading. A tree published before this existed has no file, and then
// the numbers wait for the queries as they used to.
// Naming `grid` or `checks` here as a fallback would undo the whole point: Observable
// resolves a cell's inputs from the names in it, so one mention makes this wait for the
// engine. The tree and the pages are published by the same workflow, so the file is there;
// `?data=` pointed at an older tree is the one case where it is not, and that says so
// rather than pretending the template has no cells.
const numbers = await headline;
const precomputed = Object.keys(numbers).length > 0;
const counted = numbers[code];
const cellCount = counted ? counted[0] : 0;
const off = counted ? counted[3] : 0;

const count = (number, what, quiet = false) => html`<div class="card ${quiet ? "quiet" : ""}">
  <span class="big">${number}</span><span class="what">${what}</span></div>`;

display(!precomputed
  ? html`<p><em>The tree this page is reading was published before the counts were, so the
      numbers are in the tables below rather than up here.</em></p>`
  : !counted
  ? html`<p><em>${code} is a ${framework} template, and it has no reportable cells in DPM
      ${release}: a template is introduced and withdrawn. Try another release.</em></p>`
  : html`<div class="counts">
      ${count(cellCount.toLocaleString("sv"), "reportable cells")}
      ${count(counted[1], "dimensions")}
      ${count(counted[2], "validation rules")}
      ${count(off, "switched off", off === 0)}
    </div>
    <p>${framework}, in DPM ${release} — the query's answer, asked again when you change
      the release above.</p>
    ${openness.length === 0
      ? ""
      : html`<p class="open-table"><strong>An open table.</strong> The reporter adds the
          ${openness.join(" and the ")}, so the ${cellCount.toLocaleString("sv")} cells
          below are the shape of what is filed rather than the size of it — one
          ${openness[0] === "rows" ? "row" : openness[0].replace(/s$/, "")} per thing
          reported, as many as there are.</p>`}`);
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
  // Only the narrow columns are given a width. Under `table-layout: fixed` the rest share
  // what is left, so the table is always exactly as wide as the page and the labels - the
  // sentences a reader came for - take whatever that leaves. Giving every column a width
  // instead made the table wider than the page, which hid the last two columns entirely.
  width: {row_code: 50, column_code: 45, cell: 170, datapoint: 80},
  select: false,
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
  // Three languages of the same sentence, so the three share the rest equally.
  width: {row: 50, from: 60},
  select: false,
})
```

```js
// An empty html template literal evaluates to null, and display(null) writes the word
// "null" onto the page. Nothing is displayed by not calling display.
if (reworded.numRows > 0) display(html`<h3>Rows the regulation has reworded</h3>
  <p>The datapoint did not change and neither did the cell. The sentence did.</p>
  ${Inputs.table(reworded, {columns: ["row", "celex", "en"], rows: 8, select: false,
                            width: {row: 50, celex: 165}})}`);
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
  width: {row: 50},
  select: false,
})
```

## What it breaks down by

<details class="why">
<summary>Why the wording matters</summary>
<p>The members are in the model's own wording, which is the wording a query has to match: a
near miss matches nothing rather than erroring, and a trailing space is a real
difference.</p>
</details>

```js
Inputs.table(dimensions, {
  columns: ["dimension", "members", "wording"],
  rows: 8,
  // The wording is what a query has to match, so it gets what the other two leave.
  width: {dimension: 220, members: 70},
  select: false,
})
```

## What has changed

<details class="why">
<summary>Where this comes from</summary>
<p>The EBA ships no account of this — the DPM's <code>ChangeLog</code> table is present and
empty in every release — so it is read off the version rows.</p>
</details>

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
                                     header: {row_code: "row"}, rows: 10, select: false,
                                     width: {row_code: 50, from_release: 90, to_release: 80}})}`);
```

## What checks it

<details class="why">
<summary>Why <code>active</code>, and why every code is a link</summary>
<p><code>active</code> is the EBA's deactivated-rules list. A description telling a reader
to satisfy a rule nobody runs is worse than one naming none. A code is not a stable
statement either — 2 005 of 7 514 consecutive versions of a rule change the expression — so
each links to what it checks under this release.</p>
</details>

```js
const whichRules = view(Inputs.search(checks, {placeholder: "a rule code, a severity, a module…"}));
```

```js
Inputs.table(whichRules, {
  rows: 12,
  select: false,
  width: {rule_code: 100, severity: 80, active: 60, module: 120},
  format: {
    rule_code: (d) => html`<a href="https://oluies.github.io/om-eba-annotatedtpl/?q=rule&rule_code=${d}&release=${release}">${d}</a>`,
  },
})
```
