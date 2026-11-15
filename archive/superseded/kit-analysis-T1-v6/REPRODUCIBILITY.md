Fresh-output verification

Ran python main.py from the extracted project and again after removing all generated output. Six key CSV/JSON outputs matched byte-for-byte: dashboard_runs.csv, dashboard_runs_enriched.csv, date_review.csv, extra/run_features.csv, extra/oxygen_sensitivity.csv, extra/evidence_snippets.json. The original V5 dashboard CSV also matched byte-for-byte, and every bundled raw table and metadata/FAQ file matched the supplied V5 archive. This is a local reproducibility check, not the live NASA or scientific validation.
