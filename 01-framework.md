# PAY 4.2 (FRPPAY 4.2) — framework overview

Transcribed from EBA PAY 4.2 (FRPPAY 4.2) annotated table layout, 2026-01-06.

## What this framework is

PAY 4.2 is the EBA reporting framework for **payment and fraud statistics under PSD2**.
Payment service providers report, per reporting period, the volume and value of payment
transactions and the subset of those that were fraudulent, broken down by payment
instrument, authentication method, initiation channel, counterparty geography and fraud
event type.

## Shape of the data

- **14 templates**, paired: a `.01` template reports transactions and the
  matching `.02` template reports the monetary losses due to fraud for the same instrument.
- **Up to 6 variants per `.01` template**, one sheet each, being the cross product of
  2 metrics (amount of payment, number of transactions) and 3 geographies (domestic,
  cross-border within the EEA, cross-border outside the EEA).
- **1830 datapoints** in total, each with a stable numeric id.

| Template | Subject | Reports | Variants | Datapoints |
|---|---|---|---|---|
| `Y_01.01` | Credit transfers transactions | transactions | 6 | 324 |
| `Y_01.02` | Losses due to fraud for credit transfers | losses | 1 | 3 |
| `Y_02.01` | Direct debits transactions | transactions | 6 | 60 |
| `Y_02.02` | Losses due to fraud for direct debits | losses | 1 | 3 |
| `Y_03.01` | Card-based payment transactions reported by the issuing payment service provider | transactions | 6 | 480 |
| `Y_03.02` | Losses due to fraud for card-based payment reported by the issuing payment service provider | losses | 1 | 3 |
| `Y_04.01` | Card-based payments transactions reported by the acquiring payment service provider | transactions | 6 | 444 |
| `Y_04.02` | Losses due to fraud for card-based payments reported by the acquiring payment service provider | losses | 1 | 3 |
| `Y_05.01` | Cash withdrawals using cards transactions reported by the card issuer’s payment service provider | transactions | 6 | 72 |
| `Y_05.02` | Losses due to fraud for cash withdrawals using cards reported by the card issuer’s payment service provider | losses | 1 | 3 |
| `Y_06.01` | E-money payment transactions | transactions | 6 | 312 |
| `Y_06.02` | Losses due to fraud for e-money payment transactions | losses | 1 | 3 |
| `Y_07.01` | Money remittance payment transactions | transactions | 6 | 12 |
| `Y_08.01` | Transactions initiated by payment initiation services providers | transactions | 6 | 108 |

## Axes

A datapoint is pinned down by 14 possible dimensions drawn from
4 domains, plus one of 3 metrics. See
`03-glossary/`.

## What is not in here

The layout carries labels, codes and structure. It does **not** carry the regulatory
definitions, the validation rules between datapoints, or the submission schedule.
For those, go to EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended).
