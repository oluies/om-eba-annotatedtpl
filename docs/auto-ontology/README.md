# NVIDIA auto-ontology against this pack — a trial, not a dependency

Written 5 November 2026. Staged and ready to run; nothing has been started yet, because
starting it needs one thing this directory deliberately does not contain: the address of
the on-premise inference endpoint.

[`NVIDIA/auto-ontology`](https://github.com/NVIDIA/auto-ontology) (Apache-2.0, 6.7k stars,
not accepting external contributions) reads metadata out of a relational database,
profiles its columns and samples values, has a model name the business terms, infer the
joins and propose SQL attributes, writes all of it to Postgres with pgvector embeddings,
and then answers questions in natural language by generating SQL. People certify the terms
afterwards in its UI.

## Why it is interesting here, and why not for the obvious reason

It infers what this pack already has from the source. The terms, the relationships and the
column descriptions are published by the EBA; letting a model derive "Trusted beneficiary
(Art.13 RTS)" from a column named `Y0101_r0190_c0020` is at best right by accident, and
`02-agent-instructions.md` tells an agent in as many words not to invent a definition. So
the interesting direction is the opposite one:

1. **Measure what the annotated layout is worth.** Point it at `pay42.duckdb` with nothing
   but the schema, let it derive an ontology for `Y_01.01`, and compare against the pack's
   1 830 datapoints and 93 terms. We hold the answer key, so the result is a number rather
   than an impression — the same shape of experiment as `source/score_translation.py`,
   which already scores a local translation model against the Official Journal's own
   wording.
2. **Let the pack be the certified layer.** Its certify step, and the Apache Ossie YAML
   import behind Settings → Import / Export, are where the pack's terms and SQL attributes
   fit. Then its question-to-SQL half is usable without a model having guessed the
   semantics.

Its ontology is not OWL, RDF, Turtle or SKOS, which is worth knowing before anyone plans a
route from here to a published vocabulary: it lives in Postgres, and what travels between
instances is Ossie YAML.

## The data line

Ingestion profiles columns and samples values. On a supervisory warehouse that is a
governance question, not an engineering one, and the answer there is no while inference is
hosted. Two things keep this trial on the right side of it:

- **Inference stays on premise.** `onprem.env.fragment` points every model role at a local
  OpenAI-compatible endpoint. No `nvapi-` key, no `integrate.api.nvidia.com`, and no
  `KUMO_RFM_API_KEY`, which is what would otherwise route predictive questions to a hosted
  service.
- **The source is public EBA material.** `pay42.duckdb` is built by
  `source/build_duckdb.py` from the committed CSVs: 1 830 PAY datapoints, 93 glossary
  terms, the validation rules. Not one reported figure. It is mounted `:ro`, and the
  connector opens it `read_only=True` of its own accord
  (`auto_ontology/connectors/duckdb.py`).

## What the on-premise endpoint has to serve

The configuration is five triplets — `<ROLE>_ENDPOINT`, `_API_KEY`, `_MODEL` — and each
field falls back to `DEFAULT_MODELS_<field>` when unset. One chat model therefore covers
three roles: the default, `REASONING` and `NON_REASONING`. We run
`nvidia/nemotron-3.5-super-vl-120b-a12b`.

Two roles are not chat models and cannot inherit it:

| Role | Needed? | Why |
|---|---|---|
| `EMBED` | **yes, explicitly** | Unset fields fall back to the chat model, which would then be sent to `/v1/embeddings`. Retrieval is pgvector, so ingestion and every later query must use the same embedding model or the vectors are not comparable. |
| `RERANK` | no, it fails soft | `auto_ontology/utils/rerank.py` raises on an endpoint error, and its one non-test caller — `semantic/bridge_tables.py`, choosing which term owns a bridge table — logs and falls back to the first candidate. It also appends `/v1/ranking` itself unless the URL already ends in `/rerank`, `/ranking` or `/reranking`, and speaks the NIM schema (`passages`, scored by `logit`). |

The one capability the whole ingestion chain depends on is **structured output**. The
project's own README says to use models that support it. That is what `probe_onprem.sh`
checks first, because it costs seconds and the alternative is finding out after five
containers are up.

## Running it

```sh
# 1. Do the three roles actually answer? Four calls: /models, chat with
#    response_format json_schema, /embeddings with the dimension count, /ranking.
ONPREM_BASE=http://<host>:8000/v1 EMBED_MODEL=<embedding model> \
  sh docs/auto-ontology/probe_onprem.sh

# 2. The store the trial reads, from the committed CSVs.
uv run source/build_duckdb.py

# 3. The checkout, kept out of this repository.
git clone --depth 1 https://github.com/NVIDIA/auto-ontology.git /tmp/auto-ontology
mkdir -p /tmp/auto-ontology/data && cp pay42.duckdb /tmp/auto-ontology/data/
cp .env.example /tmp/auto-ontology/.env    # then append this directory's fragment
cat docs/auto-ontology/onprem.env.fragment >> /tmp/auto-ontology/.env
cp docs/auto-ontology/docker-compose.onprem.yml /tmp/auto-ontology/

# 4. Five services: frontend :3000, backend :3001, ingestion :3002, MCP :3003,
#    Postgres 17 + pgvector :5432.
cd /tmp/auto-ontology && docker compose \
  -f docker-compose.yml -f docker-compose.onprem.yml up -d --build
```

`.env` still needs its own secrets filled in — `AUTH_SECRET`, `POSTGRES_PASSWORD`,
`AUTO_ONTOLOGY_ADMIN_PASSWORD`, `PGADMIN_PASSWORD`. The fragment only sets the model
triplets and `CONNECTION_STRINGS`.

The quickstart in the project's own README seeds a sample Wide World Importers database
from a second repository, `NVIDIA/auto-ontology-eval`. None of that is needed here: the
source is the DuckDB file, through `CONNECTION_STRINGS=duckdb:///data/pay42.duckdb`.
DuckDB and SQLite are the two engines that cannot be added in its UI, so the connection
string is the only way in for them.

## Files

| | |
|---|---|
| `onprem.env.fragment` | The five model triplets against `${ONPREM_BASE}`, plus the DuckDB connection string. Placeholders only — no address, no key. |
| `docker-compose.onprem.yml` | Mounts the store read-only into the two services that touch a source: `ingestion-service` reads the schema, `auto-ontology` runs the generated SQL. |
| `probe_onprem.sh` | The four endpoint calls above, before anything is built. |

## What would make this a dependency rather than a trial

Nothing yet. If experiment 1 says the derived ontology is close to the published one, that
is interesting and changes nothing about how the pack is built. If experiment 2 works —
the pack's terms imported as the certified layer — then there is a question worth asking
about whether question-to-SQL over the warehouse belongs in this repository or beside it.
Until then this directory is a note with its configuration attached.
