---
title: What this is
---

# The EBA data point model, by template

```js
const catalogue = await FileAttachment("./data/catalogue.json").json();
const published = await FileAttachment("./data/releases.json").json();
```

One page per reporting template, generated from the EBA's DPM 2.0 database:
**${catalogue.length} templates**, each answering what it is, what it breaks down by, and
what checks it — under any of the ${published.length} published releases, asked again when
you change it.

It is for whoever has to fill a template in and wants to know what a cell means, whether
the rule that will reject their file is still switched on, and whether the column they
have been keying a time series on has always meant the same thing.

## Two things worth knowing before you read a page

**A datapoint is not its coordinate.** The DPM has two reference systems: `VariableID`,
the identity of a datapoint, and the table coordinate — template, row, column, sheet —
which is where it sits in one version of one template. Within a release the coordinate is
unambiguous. Across releases it is not: coordinates have been reused for different
datapoints. Key a time series on `r0550_c0020` and you are keying on an address.

**Nobody wrote the descriptions.** Every description here is composed from the template
name, the row label and the column label, because the model holds no sentence for a
datapoint. That is not a shortcut taken here; it is what the model contains.

## Find a template

```js
const search = view(Inputs.search(catalogue, {placeholder: `one of ${catalogue.length} templates…`}));
```

```js
Inputs.table(search, {
  columns: ["code", "name", "modules"],
  header: {code: "template", name: "name", modules: "filed in"},
  format: {
    code: (d) => html`<a href="./t/${d}">${d}</a>`,
    modules: (d) => (d ?? []).join(", "),
  },
  width: {code: 110},
  rows: 20,
})
```

## Or by what you file

```js
// The module is the submission: own funds, leverage, large exposures, LCR and NSFR go in
// separately, and a reader who has to fill one in knows which. 312 codes in one run is a
// list nobody can navigate; this is the grouping they already have.
const filings = new Map();
for (const template of catalogue) {
  for (const module of template.modules ?? []) {
    if (!filings.has(module)) filings.set(module, []);
    filings.get(module).push(template);
  }
}
const ordered = [...filings].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0]));
```

```js
display(html`<div class="filings">${ordered.map(([module, templates]) => html`<details>
  <summary>${module} <span class="how-many">${templates.length} templates</span></summary>
  <div class="codes">${templates.map((template) => html`<div>
    <a href="./t/${template.code}">${template.code}</a> <span>${template.name}</span>
  </div>`)}</div>
</details>`)}</div>`);
```

A template is often in more than one: `C_00.01` says what kind of report this is, so it
heads every COREP submission. The counts therefore add up to more than ${catalogue.length}.

## Where the rest is

- [Ask a question](https://oluies.github.io/om-eba-annotatedtpl/) — the same model, queried in your browser, with the SQL shown next to every answer, and a small model that turns a question into one of eleven.
- [The source](https://github.com/oluies/om-eba-annotatedtpl) — the generators, the lookup tools and these pages.
