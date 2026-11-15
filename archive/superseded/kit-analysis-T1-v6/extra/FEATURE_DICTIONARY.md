V6 additive data dictionary

- dashboard_runs.csv: preserved V5 interface. dashboard_runs_enriched.csv: same rows plus traceable x_ features. Per-PSI clean tables use x_ prefix for date columns to comply with the team schema.
- x_as_run_id is the execution sequence in BASS; x_test_id is the planned test identifier. They are not interchangeable or unique on their own. Use run_id.
- x_material_family_context is an optional PI/FAQ-based family hypothesis; x_material_family_keyword is the original conservative label. Never report the inferred label as observed composition.
- x_air_listed_values_json retains order of literal numbers only for complete numeric lists. Qualified strings, ranges, pot values and text are excluded rather than stripped; raw retained. No timing, steady state, extinction or local airflow asserted. PSI-25 FAQ states cm/s and ~1 min instrument response; PSI-26 unit unconfirmed. Fan display and flow restriction are separate.
- x_co/ co2 phase status, valid_value, lower_bound: exact physically nonnegative numerics only; CO OR is >1000 ppm per FAQ, >500 is explicit lower bound. Over unspecified remains unknown; negatives kept raw. No imputation. CO2 units as source (% by volume).
- x_o2_change_pp: final minus initial calibrated oxygen, percentage points, not a combustion rate. Review flag unchanged.
