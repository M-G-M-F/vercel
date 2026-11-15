# Findings: PSI-20 ACME BRE

Transcribed into the team one-line format by the integrator from Khaled Adawi's `eda/findings.md` (Task 05).
Statements, labels, sources and caveats are his words from `eda/findings.md`, `eda/eda_summary.md` and
`table_audit/report_reconciliation.md`; nothing was added. IDs F-T5-1 to F-T5-6 were assigned for the website
(his finding 5 carries two labels and became F-T5-5 and F-T5-6). He gave no confidence levels: "not stated".
"OBSERVED IN LOCAL FILES" is written as the team label OBSERVED IN DATA.

Format: `F-<track>-<number> | statement | label | source file | row or page | confidence | caveat`

F-T5-1 | 18 summary days contain 194 recorded flames ignited; day-level counts range from 0 to 21. | OBSERVED IN DATA | PSI-20/Experimental table/PSI-20_Experimental table_ACME BRE.csv | rows 2-19 (Flames Ignited) | not stated | Day-level Flames Ignited counts do not equal raw CSV run counts.
F-T5-2 | The largest recorded day is CSV 2020-12-05 with 21 ignitions (CSV row 13); NASA Table 1 lists Test Day 20279 as 2020-10-05, also 21. | OBSERVED IN DATA | PSI-20/Experimental table/PSI-20_Experimental table_ACME BRE.csv; ACME/BRE Final Report (2022) | CSV row 13; report PDF page 24 | not stated | This is a source-date discrepancy, not an authorized correction.
F-T5-3 | Fuel-bottle categories vary across summary days, but the summary table does not link individual flames to unique oxygen settings. | OBSERVED IN DATA | PSI-20/Experimental table/PSI-20_Experimental table_ACME BRE.csv | rows 2-19 (Fuel Bottle, Oxygen Conc (percent)) | not stated | Oxygen concentration entries are lists of approximate conditions on each day, not per-flame settings. CSV row 6 contains 3400% and row 9 contains 2100%; both are retained and excluded from any numeric oxygen analysis.
F-T5-4 | Run 19056A2 has 31,316 raw samples and a 123.034-second timestamp gap. | OBSERVED IN DATA | 19056A2_data.csv (BRE raw run) | metadata/header rows 1-2, data rows 3-31318 (Time, IonCurrent, PMT1, MFCA3FuelFlow) | not stated | The plotted channels vary over time; raw units are unspecified. Clock synchronization and timezone unverified. A raw signal trace shows variation and a recording gap, not flame stability, extinction, or causal relationships.
F-T5-5 | Final Report PDF pages 110 and 116 say 194 flames ignited, whereas pages 29 and 127 mention 196 successful ignitions. | REPORTED BY NASA OR A PUBLICATION (ACME/BRE Final Report, 2022) | ACME/BRE Final Report (2022) | PDF pages 29, 110, 116, 127 | not stated | Page 127 invokes Round 2, whereas page 110 reports 132 Round 2 flames: an additional apparent scope inconsistency.
F-T5-6 | The 194 versus 196 discrepancy remains unresolved; the figures must not be treated as equivalent counts. | OUR INFERENCE | ACME/BRE Final Report (2022); PSI-20/Experimental table/PSI-20_Experimental table_ACME BRE.csv | PDF pages 29, 110, 116, 127; CSV rows 2-19 | not stated | The CSV sum 194 agrees numerically with the NASA total on pages 110 and 116; this does not prove equivalence of counting definitions.
