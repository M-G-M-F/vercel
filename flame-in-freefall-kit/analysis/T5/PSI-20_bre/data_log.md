# Data log — PSI-20 / 19056A2

## Inputs (OBSERVED IN DATA)
- data: `19056A2_data.csv`; 11228564 bytes; SHA-256 `9b90a1c2b0c227823df193ba0a070d07bb30e42077fb0534ca38bc47687dad49`; 31316 measurement records; 36 columns
- mfc: `19056A2_mfcSetpoints.csv`; 2846 bytes; SHA-256 `caea72a8b47536d3adb9266e5a4c6bd0403d9c1e0533267b5cc70425b599590f`; 60 measurement records; 4 columns

## Transformations
- Read raw bytes; decode UTF-8-SIG, fall back to Latin-1 only on decoding failure.
- CSV record 1 preserved as ordered metadata fields; record 2 used as headers.
- Original row order and repeated timestamps retained; conversion errors counted, not dropped.
- Parse date from metadata first field and time-of-day from Time, without timezone or midnight rollover.
- MFC change-event IDs assigned only to setpoint changes; first row is initial state, repeated rows are not independent events.
- Charts use selected raw numeric channel values, no calibration.
- Optional backward as-of timestamp preview: last MFC row at or before each data timestamp, no tolerance, stable sort, equal timestamps resolve to last source-order MFC row. This is a visualization aid, NOT a measured synchronized state; rows with invalid timestamps excluded from preview only.

## Uncertainties / limitations
- MFC clock synchronization with sensor clock is UNVERIFIED. Events inside data gaps are timestamp-label observations only.
- Alignment preview retains source row IDs and all data rows, including invalid timestamps, and is NOT a measured MFC response.
- Metadata field labels are preserved, but sensor calibration and physical meanings have not been independently verified against NASA documentation.
- Experiment calendar dates must agree across source metadata; timezone, clock synchronization, possible rollover, and actual acquisition sampling behavior are undocumented.
- Non-modal positive intervals are reported without asserting expected sample rate.
- No extinction outcome or scientific causality can be established from this audit.

## Task 03 — inventory extension
- Added `scripts/build_run_inventory.py` and synthetic inventory regression tests; Task 02B audit and source CSVs are unchanged.
- Metadata and headers read with streaming CSV reader; recognized files hashed in blocks. Source data records not loaded for inventory.
- Filename-derived candidate IDs compared to `Test Point`, calendar dates compared across unique candidates, and duplicates never auto-resolved.
- No expected-run list provided; no claims of missing NASA runs. Inventory outputs exclude source data and are limited to locally present files.

## Task 03B — run-ID compatibility patch
- Inventory filename recognition and expected-run manifest validation now share the same safe run-ID grammar: `[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*`.
- Malformed run-like CSV filenames are logged in file inventory and pairing issues, rather than silently classified as unrelated. Their contents are not treated as validated run data.
- Nine synthetic regression tests added. Existing 19056A2 local inventory outputs reproduced byte-for-byte (6/6) against Task 03 ZIP.
- Local source CSV hashes unchanged. `19051K1_1` examples are synthetic only; no claim of independently verified NASA CSV filenames or metadata.

## Task 04 — experimental table audit (2026-11-15)
- **OBSERVED IN LOCAL FILES:** Source `/mnt/data/PSI-20_Experimental table_ACME BRE.csv`; SHA-256 `4aa5d3f98708ceacced5c620d46858b9965f8d4d941b203229f46467d53e5ab7`. Original source remains unchanged.
- **OBSERVED IN LOCAL FILES:** 18 day-level records, 8 columns, valid `Flames Ignited` sum 194; unusual raw oxygen tokens `3400%` and `2100%`; no normalization or unit conversion.
- **OBSERVED IN LOCAL FILES:** Local Task 03B run inventory links `19056A2` (metadata calendar date `2019-02-25`) to one summary day; 17 summary rows have no matching locally validated run. Not a claim about NASA run completeness.
- **OUR INFERENCE:** Exact calendar date equality is candidate linkage only. Table note says ISS day change neglected; timezone and operational day boundaries are not resolved.
- **REPORTED BY NASA:** No independently page-verified external NASA numerical total used; no reconciliation asserted.
- Transformations: strict UTF-8-sig CSV reader, preserve raw string values and original row numbers, parse calendar dates for matching, validate nonnegative integer count cells, flag percent tokens over 100, report formatting and missing cells. Outputs generated in `table_audit/`; no source mutation.
- Uncertainties: table authorship not independently authenticated; oxygen token intent, flame/run semantics, date convention, expected runs, chamber pressures, and independent comparable NASA report/page.

## Task 04B — NASA report cross-source reconciliation (2026-11-15)
- Source CSV: `/mnt/data/PSI-20_Experimental table_ACME BRE.csv` SHA-256 `4aa5d3f98708ceacced5c620d46858b9965f8d4d941b203229f46467d53e5ab7` (unchanged).
- Independently inspected source: **ACME/BRE Final Report (2022)**, 1 Feb. 2022, PDF pages 24, 110, 112, 116, 127. Reference table transcription is stored with page-level provenance and no inferred raw-run identities.
- OBSERVED IN LOCAL FILES: 18 summary rows, `Flames Ignited` sum 194; source oxygen text `3400%` and `2100%`; CSV dates 2020-10-17 and 2020-12-05.
- REPORTED BY NASA: Table 1 pages 24/112 oxygen 34% and 21%, dates 2020-09-17 and 2020-10-05 for documented Test Days. Page 110 and 116 state 194 flames; page 127 states "Round 2 tests were finished with 196 successful ignitions". Table 1 page 24 versus 112 disagrees on Test Day 19094 (Apr. 4 vs Apr. 5).
- OUR INFERENCE: Source text differences do not establish wrong measurements; the 194/196 difference may reflect scope/definitions and remains unresolved. No normalization, raw-run mapping, calibration, modeling, extinction classification or causal claims.
- Outputs: separate report manifest, discrepancy CSV, notes and self-excluding SHA-256 inventory. Prior Task 04 outputs not overwritten.

## Task 04C — source interpretation patch (2026-11-15)
- **REPORTED BY NASA:** *ACME/BRE Final Report (2022)* PDF page 23 explicitly corrects Test Day 19094 to April 4, 2019 (operational test-day start); page 24 reflects April 4, page 112 retains superseded April 5. Both dates are preserved with page-level provenance.
- **REPORTED BY NASA:** page 29 says 196 successful ignitions for orbital BRE tests; page 110 states 62 Round 1 plus 132 Round 2 equals 194 total flames; page 116 states 194 flames ignited; page 127 states 196 successful ignitions with Round 2 wording.
- **OUR INFERENCE:** the 194/196 count and page-127 Round 2 scope are unresolved; no equivalence or causal/physical interpretation asserted.
- **OBSERVED IN LOCAL FILES:** original CSV unchanged; four cross-source differences preserved; historical date discrepancy reclassified as explained. Updated only reconciliation module, its tests, reconciliation products, README and data log.
