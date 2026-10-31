# A read-only API, and DCAT-AP-SE — parked

Written 31 October 2026. Parked pending one question that is not technical: **can we have a
server?** Everything below is either already true, or costed and ready to build.

## What is already true

The published tree is a read-only API for anyone holding DuckDB. Measured from a laptop
against the live site:

```sql
INSTALL httpfs; LOAD httpfs;

SELECT row_code, row_label
FROM 'https://oluies.github.io/om-eba-annotatedtpl/data/4.4/cells/framework=COREP/data_0.parquet'
WHERE table_code = 'C_03.00';                               -- 0.16 s

SELECT template, row, sv
FROM 'https://oluies.github.io/om-eba-annotatedtpl/data/its_labels/framework=COREP/data_0.parquet'
WHERE template = 'C_03.00';                                 -- 0.07 s, "Kärnprimärkapitalrelation"
```

The gzip hazard that forced the browser pages to fetch whole files (see the README) is a
DuckDB-WASM problem; the native httpfs handles the same URLs correctly.

So the data is already served. What is missing is a *contract*: nothing promises those
paths will not move, and nothing describes them to a reader who does not already know.

## What a static site can and cannot be

**Can:** fixed resources at stable paths, generated at publish time, cached by the CDN,
with no process to run and nothing to keep up. A JSON file per template per release, an
index, and an `openapi.json` that describes them is a real REST API by every definition
that matters to a consumer.

**Cannot:** query parameters. `GET /templates?framework=COREP&dimension=…` needs something
that runs. A static API is "fetch this thing", not "find me the things where".

**GraphQL: not without a server.** GraphQL is a resolver; there is no static form of it. It
would be a service — FastAPI or Strawberry over this same parquet tree — and then hosting,
uptime and access control become somebody's job. That is the decision this note is parked
on, and it is an operations question rather than an engineering one.

## The three pieces, in the order they are worth building

1. **`openapi.json` and a documented URL contract** over what already exists. Cheapest, and
   it turns the tree into an API on purpose rather than by accident.
2. **A JSON file per template**, for consumers without DuckDB. Roughly 327 templates × 3
   releases; the large ones need splitting (C_13.01 has 6 839 cells), so a summary document
   plus a cells document rather than one of everything.
3. **`dcat.rdf`**, described below.

## DCAT-AP-SE, as it actually stands

Read from docs.dataportal.se on 31 October 2026.

- Current version is **DCAT-AP-SE 3.0.1, published 25 November 2024**, a Swedish profile of
  DCAT-AP 3.0.0, itself a profile of W3C DCAT 3. Editor: Matthias Palmér (DIGG and
  MetaSolutions). The specification is CC-BY 4.0.
- Harvesting reads **one URL** and expects **RDF/XML**. A single static file over HTTPS is a
  valid source. Harvests run daily, around 04:00, and a re-harvest can be forced.
- Blank nodes are not allowed for catalogue, dataset, distribution, publisher or contact.
  Every one needs an absolute IRI in a namespace we control.
- There is a validator in the sandbox: `https://sandbox.admin.dataportal.se/toolkit/catalog`.

Three things that are obstacles rather than formalities:

- **The catalogue metadata must be CC-0.** The data is derived from EBA material, which may
  be reproduced "provided the source is acknowledged" — that is not one of the standard
  open-licence URIs the quality score is computed against. What licence URI to put on the
  distributions is a question for whoever publishes, not a field to fill in.
- **The publisher URI is `http://dataportal.se/organisation/SE<orgnr>`**, which assumes an
  organisation number. Public authorities are *pre-registered* with a harvest source of the
  form `http://<authority>.se/datasets/dcat`. So if this is ever harvested it is published
  by FI, from an FI address — not from a personal GitHub Pages site. That is an FI decision
  and the technical work is the easy part of it.
- The specification's own tables of mandatory properties are rendered by script and could
  not be read programmatically, so nothing here claims conformance. The way to find out is
  to build the file and run it through the sandbox validator.

## What would change if we do get a server

The parquet tree stays exactly as it is — it is the storage either way. A server adds:
query parameters and GraphQL over the same files; content negotiation, so one URL can
answer in JSON, CSV or RDF; and an access log, which is the only way to learn which
templates people actually read. None of that requires rebuilding anything described above,
which is why building piece 1 now costs nothing if the answer later is yes.
