# PAY 4.2 glossary — domains and members

Controlled vocabulary of the EBA PAY 4.2 (FRPPAY 4.2) framework, transcribed from
EBA PAY 4.2 (FRPPAY 4.2) annotated table layout, 2026-01-06; datapoint ids from the DPM 2.0 database, module PSD_FRP 1.1.0.

A **domain** is a set of allowed values. A **dimension** is an axis that draws its
values from one domain — several dimensions share a domain, which is why a member code
alone does not tell you which dimension it belongs to. The member's position in the
layout does.

**Definitions.** The labels below are transcribed verbatim from the annotated table layout. They are the framework's own wording, not a legal definition. Where a precise definition is needed, cite EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended) rather than paraphrasing this file.


## Domain `GA` — Geographical breakdown

3 members, used by 1 dimension(s): `PTG` Payment transactions geographical breakdown

| Member | Label | Used as dimension | Templates |
|---|---|---|---|
| `qx2010` | Domestic | Payment transactions geographical breakdown | Y_01.01, Y_02.01, Y_03.01, Y_04.01, Y_05.01, Y_06.01, Y_07.01, Y_08.01 |
| `qx2011` | European Economic Area (EEA) | Payment transactions geographical breakdown | Y_01.01, Y_02.01, Y_03.01, Y_04.01, Y_05.01, Y_06.01, Y_07.01, Y_08.01 |
| `qx2012` | Non-European Economic Area (EEA) | Payment transactions geographical breakdown | Y_01.01, Y_02.01, Y_03.01, Y_04.01, Y_05.01, Y_06.01, Y_07.01, Y_08.01 |

## Domain `qET` — Fraud event types

12 members, used by 1 dimension(s): `qEEB` Event Type

| Member | Label | Used as dimension | Templates |
|---|---|---|---|
| `qx2062` | Card details theft | Event Type | Y_03.01, Y_04.01 |
| `qx2059` | Card not received | Event Type | Y_03.01, Y_04.01, Y_05.01 |
| `qx2056` | Counterfeit card | Event Type | Y_03.01, Y_04.01, Y_05.01 |
| `qx2053` | Issuance of a payment order by the fraudster | Event Type | Y_01.01, Y_03.01, Y_04.01, Y_05.01, Y_06.01 |
| `qx2058` | Lost or stolen card | Event Type | Y_03.01, Y_04.01, Y_05.01 |
| `qx2064` | Manipulation of the payer by the fraudster to consent to a direct debit | Event Type | Y_02.01 |
| `qx2055` | Manipulation of the payer by the fraudster to issue a payment order | Event Type | Y_01.01, Y_06.01 |
| `qx2061` | Manipulation of the payer to make a card payment | Event Type | Y_03.01, Y_04.01 |
| `qx2060` | Manipulation of the payer to make a cash withdrawal | Event Type | Y_05.01 |
| `qx2054` | Modification of a payment order by the fraudster | Event Type | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2057` | Other issuance of a payment order by the fraudster | Event Type | Y_03.01, Y_04.01, Y_05.01 |
| `qx2063` | Unauthorised payment transactions | Event Type | Y_02.01 |

## Domain `qPY` — Payment transaction characteristics

31 members, used by 9 dimension(s): `qBOM` Type of authentication, `qBXW` Type of payment channel, `qCYY` Card funtion in payment, `qKJI` Form of payment, `qKJJ` Payment issued/acquired, `qRCA` Reasons for authentication via non-strong customer authentication, `qTCO` Type of consent of payment, `qTII` Type of initiation of payments, `qZZV` Type of payment transaction

| Member | Label | Used as dimension | Templates |
|---|---|---|---|
| `qx2010` | Acquired | Form of payment; Payment issued/acquired | Y_04.01, Y_04.02 |
| `qx2027` | Authenticated via non-strong customer authentication | Type of authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01, Y_08.01 |
| `qx2026` | Authenticated via strong customer authentication | Type of authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01, Y_08.01 |
| `qx2009` | Card | Form of payment; Payment issued/acquired | Y_03.01, Y_03.02, Y_04.01, Y_04.02 |
| `qx2001` | Cash withdrawals | Form of payment | Y_05.01, Y_05.02 |
| `qx2030` | Consent given in another form than an electronic mandate | Type of consent of payment | Y_02.01 |
| `qx2031` | Consent given via an electronic mandate | Type of consent of payment | Y_02.01 |
| `qx2042` | Contactless low value | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2005` | Credit transfers | Form of payment | Y_01.01, Y_01.02, Y_08.01 |
| `qx2012` | Direct debits | Form of payment | Y_02.01, Y_02.02 |
| `qx2008` | E-money | Form of payment | Y_06.01, Y_06.02 |
| `qx2022` | Fraudulent payment transaction | Type of payment transaction | Y_01.01, Y_02.01, Y_03.01, Y_04.01, Y_05.01, Y_06.01, Y_07.01, Y_08.01 |
| `qx2028` | Initiated electronically | Type of initiation of payments | Y_01.01, Y_03.01, Y_04.01 |
| `qx2029` | Initiated non-electronically | Type of initiation of payments | Y_01.01, Y_03.01, Y_04.01 |
| `qx2024` | Initiated via non-remote payment channel | Type of initiation of payments; Type of payment channel | Y_01.01, Y_03.01, Y_04.01, Y_06.01, Y_08.01 |
| `qx2025` | Initiated via remote payment channel | Type of initiation of payments; Type of payment channel | Y_01.01, Y_03.01, Y_04.01, Y_06.01, Y_08.01 |
| `qx2011` | Issued | Payment issued/acquired | Y_03.01, Y_03.02 |
| `qx2033` | Low value | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2039` | Merchant initiated transactions | Reasons for authentication via non-strong customer authentication | Y_03.01, Y_04.01, Y_06.01 |
| `qx2007` | Money remittances | Form of payment | Y_07.01 |
| `qx2040` | Other reasons for authentication via non-strong customer authentication | Reasons for authentication via non-strong customer authentication | Y_03.01, Y_04.01, Y_06.01 |
| `qx2036` | Payment to self | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_06.01 |
| `qx2000` | Payment transactions | Type of payment transaction | Y_01.01, Y_01.02, Y_02.01, Y_02.02, Y_03.01, Y_03.02, Y_04.01, Y_04.02, Y_05.01, Y_05.02, Y_06.01, Y_06.02, Y_07.01, Y_08.01 |
| `qx2023` | Payment transactions other than credit transfers | Form of payment | Y_08.01 |
| `qx2044` | Payments with cards with a credit or delayed debit function | Card funtion in payment | Y_03.01, Y_04.01, Y_05.01 |
| `qx2043` | Payments with cards with a debit function | Card funtion in payment | Y_03.01, Y_04.01, Y_05.01 |
| `qx2035` | Recurring transaction | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2038` | Transaction risk analysis | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2034` | Trusted beneficiary | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_06.01 |
| `qx2041` | Unattended terminal for transport or parking fares | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_04.01, Y_06.01 |
| `qx2037` | Use of secure corporate payment processes or protocols | Reasons for authentication via non-strong customer authentication | Y_01.01, Y_03.01, Y_06.01 |

## Domain `qRP` — Payment related parties

8 members, used by 3 dimension(s): `qBAN` Type of user, `qBEA` Relationships, `qKKL` Payment related parties

| Member | Label | Used as dimension | Templates |
|---|---|---|---|
| `qx2074` | Account holder | Type of user | Y_05.02 |
| `qx2071` | Others than payment users or service providers | Payment related parties | Y_01.02, Y_02.02, Y_03.02, Y_04.02, Y_05.02, Y_06.02 |
| `qx2075` | Payee | Type of user | Y_02.02, Y_04.02 |
| `qx2076` | Payer | Type of user | Y_01.02, Y_03.02 |
| `qx2028` | Payment initiation services provider | Payment related parties | Y_01.01, Y_08.01 |
| `qx2072` | Payment service provider | Payment related parties | Y_01.02, Y_02.02, Y_03.02, Y_04.02, Y_05.02, Y_06.02 |
| `qx2083` | Payment service user | Payment related parties | Y_01.02, Y_02.02, Y_03.02, Y_04.02, Y_05.02, Y_06.02 |
| `qx2005` | Reporting entity | Relationships | Y_01.02, Y_02.02, Y_03.02, Y_04.02, Y_05.02, Y_06.02 |
