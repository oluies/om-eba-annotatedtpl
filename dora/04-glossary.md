# DORA glossary

The vocabulary behind the 85 columns, from EBA DPM 2.0 database, module DORA 1.1.0, from the EBA DPM Data Dictionary, https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary.

**Definitions.** These are the framework's own wording, not legal definitions. Where a
precise one is needed, cite the DORA Implementing Technical Standards on the register of information.

## Properties

What a column holds, and its type. 50 distinct properties across 85 columns -
so most columns have their own, which is what makes DORA a register rather than a
measurement.

| Property | Type | Columns | Used by |
|---|---|---|---|
| Additional identification code of ICT third-party service provider | string (non empty) | 1 | B_05.01 c0030 |
| Additional information | string (non empty) | 2 | B_06.01 c0060, B_07.01 c0120 |
| Alternative providers | enumeration | 1 | B_07.01 c0110 |
| Amount as defined in Annex IV of ITS on ICT TPP register | monetary | 1 | B_01.02 c0110 |
| Annual expense or estimated cost | monetary | 2 | B_02.01 c0050, B_05.01 c0100 |
| Branch/not a branch | enumeration | 1 | B_04.01 c0030 |
| Code of the currency | enumeration | 3 | B_01.02 c0100, B_02.01 c0040, B_05.01 c0090 |
| Competent authority | string (non empty) | 1 | B_01.01 c0050 |
| Contractual arrangement reference number | string (non empty) | 1 | B_02.01 c0030 |
| Counterparty nature | enumeration | 1 | B_01.01 c0040 |
| Country of location | enumeration | 1 | B_01.03 c0040 |
| Country the law of which governs the contract | enumeration | 1 | B_02.02 c0120 |
| Country where the license or registration has been issued | enumeration | 3 | B_01.01 c0030, B_01.02 c0030, B_05.01 c0080 |
| Data sensitivness | enumeration | 1 | B_02.02 c0170 |
| Date of deletion | date | 1 | B_01.02 c0090 |
| Date of integration | date | 1 | B_01.02 c0080 |
| Date of last assessment of criticality or importance of the function | date | 1 | B_06.01 c0070 |
| Date of reporting | date | 1 | B_01.01 c0060 |
| Date of the last audit | date | 1 | B_07.01 c0070 |
| End date | date | 1 | B_02.02 c0080 |
| Existence of an exit plan | enumeration | 1 | B_07.01 c0080 |
| Function is critical or important? | enumeration | 1 | B_06.01 c0050 |
| Identification code | string (non empty) | 1 | B_05.01 c0110 |
| Impact of function discontinuing | enumeration | 1 | B_06.01 c0100 |
| Impact of service discontinuing | enumeration | 1 | B_07.01 c0100 |
| Internal definitions | string (non empty) | 19 | B_99.01 c0010, B_99.01 c0020, B_99.01 c0030 |
| LEI code of the direct parent | string (non empty) | 1 | B_01.02 c0060 |
| Last date of record entry | date | 1 | B_01.02 c0070 |
| Level of reliance on the service | enumeration | 1 | B_02.02 c0180 |
| Link | true | 3 | B_02.03 c0030, B_03.01 c0030, B_03.03 c0031 |
| Name of entity | string (non empty) | 4 | B_01.01 c0020, B_01.02 c0020, B_01.03 c0030 |
| Name of entity (latin version) | string (non empty) | 1 | B_05.01 c0060 |
| Name of operational/business functions of an entity | string (non empty) | 1 | B_06.01 c0030 |
| Notice period for termination | integer | 2 | B_02.02 c0100, B_02.02 c0110 |
| Possibility of reintegration of the contracted service | enumeration | 1 | B_07.01 c0090 |
| Reason for contract termination | enumeration | 1 | B_02.02 c0090 |
| Reasons for the substituibility assessment outcome | enumeration | 1 | B_07.01 c0060 |
| Recovery point objective of the function | integer | 1 | B_06.01 c0090 |
| Recovery time objective of the function | integer | 1 | B_06.01 c0080 |
| Role of entity within and outside a group | enumeration | 1 | B_01.02 c0050 |
| Start date | date | 1 | B_02.02 c0070 |
| Storage of data | enumeration | 1 | B_02.02 c0140 |
| Substituibility assessment | enumeration | 1 | B_07.01 c0050 |
| Type of code | enumeration | 2 | B_05.01 c0040, B_05.01 c0120 |
| Type of code to identify the ICT third-party service provider | enumeration | 5 | B_02.02 c0040, B_03.02 c0030, B_05.01 c0020 |
| Type of code used to identify the subcontractor | enumeration | 1 | B_05.02 c0070 |
| Type of contractual arrangement | enumeration | 1 | B_02.01 c0020 |
| Type of entity within the scope of the register of information | enumeration | 1 | B_01.02 c0040 |
| Type of legal entity | enumeration | 1 | B_05.01 c0070 |
| Type of licenced activity | enumeration | 1 | B_06.01 c0020 |

## Domain members

Only the columns that carry a dimensional context have these: 39 of 85.
24 members across 7 domains.

### Accounting items

1 members.

| Member | Description | Columns |
|---|---|---|
| Assets | — | B_01.02 c0110 |

### Boolean total

1 members.

| Member | Description | Columns |
|---|---|---|
| Yes | — | B_06.01 c0060, B_07.01 c0120 |

### Code Lists

10 members.

| Member | Description | Columns |
|---|---|---|
| Difficult | — | B_99.01 c0150 |
| Easily substitutable | — | B_99.01 c0130 |
| Easy | — | B_99.01 c0140 |
| High | — | B_99.01 c0060, B_99.01 c0090, B_99.01 c0190 |
| Highly complex | — | B_99.01 c0160 |
| Highly complex substitutability | — | B_99.01 c0110 |
| Low | — | B_99.01 c0040, B_99.01 c0070, B_99.01 c0170 |
| Medium | — | B_99.01 c0050, B_99.01 c0080, B_99.01 c0180 |
| Medium complexity in terms of substitutability | — | B_99.01 c0120 |
| Not substitutable | — | B_99.01 c0100 |

### Contracts/Transactions

5 members.

| Member | Description | Columns |
|---|---|---|
| Overarching arrangement | — | B_02.01 c0030, B_99.01 c0020 |
| Provider | Provider of the service under the contractual arrangement | B_02.02 c0110, B_02.02 c0170, B_07.01 c0050 |
| Standalone arrangement | — | B_99.01 c0010 |
| Subsequent or associated arrangement | — | B_99.01 c0030 |
| User | User of the service under the contractual arrangement | B_02.02 c0100, B_02.02 c0180, B_04.01 c0030 |

### Currency

2 members.

| Member | Description | Columns |
|---|---|---|
| Currency used for the preparation of the entity’s financial statements | — | B_01.02 c0100 |
| Currency used to report annual expense or estimated cost | — | B_02.01 c0040 |

### Related parties/Relationships

3 members.

| Member | Description | Columns |
|---|---|---|
| Direct parent | — | B_01.02 c0060 |
| Ultimate parent | — | B_05.01 c0110, B_05.01 c0120 |
| headquarter | — | B_05.01 c0080 |

### Type of activity

2 members.

| Member | Description | Columns |
|---|---|---|
| ICT services | — | B_02.02 c0180 |
| storage (data at rest) | — | B_02.02 c0170 |
