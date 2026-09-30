# DORA — register of information

The register of information under the Digital Operational Resilience Act: which entities
report, which contractual arrangements they hold with ICT third-party service providers,
which functions those services support, and how the arrangements are assessed.

**85 datapoints across 15 templates.** Transcribed from EBA DPM 2.0 database, module DORA 1.1.0.

**Definitions.** The labels here are the framework's own wording, not a legal definition.
Where a precise definition is needed, cite the DORA Implementing Technical Standards on the register of information rather than paraphrasing this file.

## How this differs from PAY 4.2

PAY reports fixed grids: a known row, a known column, 1,830 datapoints. DORA mostly
does not. 66 of its 85 datapoints sit on **open rows** - the register holds one row
per entity, contract or provider, and the count is whatever the reporter has.

The DPM writes an open row as `r*`. A warehouse writes it as a record ordinal, commonly
`r999`. Neither is a framework row code, and neither narrows the datapoint.

Only `B_99.01` has fixed rows, 19 of them.

So for DORA the column carries the meaning and the row carries the record. That changes
the lookup, and `02-agent-instructions.md` says how.

## Templates

| Template | Table | Subject | Rows | Datapoints |
|---|---|---|---|---|
| `B_01.01` | `B_01_01` | Entity maintaining the register of information | open | 5 |
| `B_01.02` | `B_01_02` | List of entities within the scope of the register of information | open | 10 |
| `B_01.03` | `B_01_03` | List of branches | open | 2 |
| `B_02.01` | `B_02_01` | Contractual arrangements – General Information | open | 4 |
| `B_02.02` | `B_02_02` | Contractual arrangements – Specific information | open | 10 |
| `B_02.03` | `B_02_03` | List of intra-group contractual arrangements | open | 1 |
| `B_03.01` | `B_03_01` | Entities signing the Contractual arrangements for receiving ICT service(s) or on behalf of the entities making use of the ICT service(s) | open | 1 |
| `B_03.02` | `B_03_02` | ICT third-party service providers signing the Contractual arrangements for providing ICT service(s) | open | 1 |
| `B_03.03` | `B_03_03` | Entities signing the Contractual arrangements for providing ICT service(s) to other entity within the scope of consolidation | open | 1 |
| `B_04.01` | `B_04_01` | Entities making use of the ICT services | open | 1 |
| `B_05.01` | `B_05_01` | ICT third-party service providers | open | 11 |
| `B_05.02` | `B_05_02` | ICT service supply chains | open | 2 |
| `B_06.01` | `B_06_01` | Functions identification | open | 8 |
| `B_07.01` | `B_07_01` | Assessment of the ICT services | open | 9 |
| `B_99.01` | `B_99_01` | Definitions from Entities making use of the ICT Services | fixed | 19 |
