# PAY 4.2 glossary — dimensions

The 14 axes a datapoint can be broken down by. Each draws its allowed
values from one domain; see `domains-and-members.md` for the values themselves.

**Definitions.** The labels below are transcribed verbatim from the annotated table layout. They are the framework's own wording, not a legal definition. Where a precise definition is needed, cite EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended) rather than paraphrasing this file.


| Dimension | Label | Domain | Domain name | Members used | Domain size |
|---|---|---|---|---|---|
| `PTG` | Payment transactions geographical breakdown | `GA` | Geographical breakdown | 3 | 3 |
| `qEEB` | Event Type | `qET` | Fraud event types | 12 | 12 |
| `qCYY` | Card funtion in payment | `qPY` | Payment transaction characteristics | 2 | 31 |
| `qKJI` | Form of payment | `qPY` | Payment transaction characteristics | 8 | 31 |
| `qKJJ` | Payment issued/acquired | `qPY` | Payment transaction characteristics | 3 | 31 |
| `qRCA` | Reasons for authentication via non-strong customer authentication | `qPY` | Payment transaction characteristics | 10 | 31 |
| `qBOM` | Type of authentication | `qPY` | Payment transaction characteristics | 2 | 31 |
| `qTCO` | Type of consent of payment | `qPY` | Payment transaction characteristics | 2 | 31 |
| `qTII` | Type of initiation of payments | `qPY` | Payment transaction characteristics | 4 | 31 |
| `qBXW` | Type of payment channel | `qPY` | Payment transaction characteristics | 2 | 31 |
| `qZZV` | Type of payment transaction | `qPY` | Payment transaction characteristics | 2 | 31 |
| `qKKL` | Payment related parties | `qRP` | Payment related parties | 4 | 8 |
| `qBEA` | Relationships | `qRP` | Payment related parties | 1 | 8 |
| `qBAN` | Type of user | `qRP` | Payment related parties | 3 | 8 |

## Note on `Card funtion in payment`

The label is spelled that way in the source layout (`funtion`). It is transcribed
verbatim here so a search against the framework matches. Use the corrected spelling in
user-facing descriptions and keep the original as a synonym.
