# The template pages

One page per reporting template, built with [Observable Framework](https://observablehq.com/framework).

```bash
npm ci
DPM2_DB=../source/dpm2/dpm2_4_4.duckdb OBS_FRAMEWORKS="COREP FINREP" ./build.sh
```

## Why this and not a rendered document

The pages were Quarto documents, and the thing they could not do is the thing a reader
wants: **choose a release and have the page answer under it**. Quarto renders once, at
build, so a selector would mean carrying three releases' cells, rules and history in one
page — and its table of contents would still describe one of them.

Here the queries run in the reader's browser against the parquet the publish already
writes, so a different release is a different URL the page asks for. The same mechanism
gives the other thing a document could not: all 808 cells of a template, searchable, with
rows rendered as you scroll. The Quarto page showed twelve and pointed at a CSV.

It is also faster to build, for a principled reason rather than a lucky one: nothing is
computed at build, so there is no kernel per page. 154 FINREP pages take 17 seconds where
rendering them as documents took twenty minutes.

## How it fits together

- `src/t/[code].md` — **one source file for every template page**. `dynamicPaths` in
  `observablehq.config.js` says which templates exist, so adding a framework adds pages
  and a withdrawn template stops having one, without a file per template to maintain.
- `src/data/_catalogue.py` — which templates exist, and their names, from the DPM. Run
  through `catalogue.json.sh` because Observable runs a `.py` loader with whatever
  `python3` is on PATH, and that one has no duckdb.
- `build.sh` — writes the catalogue, then builds. Two steps because `dynamicPaths` is read
  when the config loads, which is before any data loader has run.
- The queries live in `source/dpm_pages.py`, shared with the markdown Quarto writes for
  the catalogue rather than written twice: a number must not mean one thing on a page and
  another in the article about it.

## What a page carries

The grid, what it breaks down by, and what checks it — each from the release the reader
picked. Then three things the DPM does not have, read by URL like the rest:

- **the same rows in Swedish and German**, from `its_labels.csv`. Not a translation: the
  templates are an annex to an Implementing Regulation and one is published in all 24
  official languages. A `from` of `stem` means the Journal printed that grid once, under
  the template this one varies.
- **rows the regulation has reworded**, where its own consolidations differ. Sixteen
  templates of 165 have any, so most pages print nothing here — which is the signal.
- **what the regulation says a row is**, from the instructions annex, with the article
  that requires it, in Swedish too.

And **what has changed** — how many of a template's datapoints have sat at another
coordinate, and which rows the EBA has reworded while the coordinate and the datapoint
stayed. That one is a comparison *across* releases rather than an answer under one, so it
cannot come from the tables the rest of the page reads: `gen_wasm_data.py` publishes
`template_changes` and `relabelled` for it. Counts rather than a list, because a reader
wants to know whether this template moved; `lookup_dpm_history` answers which datapoint
went where, one at a time.

The three below are not release-scoped the way the rest of the page is: a regulation has its own
versions, and each row carries the `celex` it came from.

## Two things that will bite

**Verify in Chrome, not Safari.** Safari 27 renders an Observable page with every cell
blank and *no error anywhere* — a pristine three-line Framework project does the same, so
it is not this code. It looks exactly like broken JavaScript. Chrome renders it correctly.

**Do not attach the partitioned parquet as files.** Our layout names every partition
`data_0.parquet`, and Observable's attachment handling collides on the basename: `cells`
came back as the three columns it shares with `cell_members`, with a binder error naming a
column that is plainly in the file. The pages read URLs instead, which has no such naming
— and which is what makes the release selector possible at all.
