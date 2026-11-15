# Archive

Files kept for reference only. Nothing in the website, the kit tools or the export tool reads this folder,
except `tools/export_rag_corpora.py`, which compares the superseded T1 pack with its replacement.
Every move is logged in `docs/REORGANIZATION_LOG.md` with its reason and SHA-256.

| Path | What it is | Why kept |
| --- | --- | --- |
| `superseded/RAG/Amr.txt` | T1 v5 deep analysis pack (283 chunks) | replaced by `RAG/Morgan_RAG_Corpus_v6/`; four chunks changed wording, kept for comparison |
| `superseded/kit-analysis-T1-template/` | the kit's unfilled T1 template | replaced by the T1 package |
| `superseded/kit-analysis-T1-v6/`, `superseded/RAG/Morgan_RAG_Corpus_v6/`, `submissions/BASS_Python_AmrProject_v6.zip` | T1 v6 package, corpora and submission | replaced by v8; the export tool compares the v6 corpora with v8 |
| `submissions/T3_nadeem_v1.zip` | first T3 submission | 15 files differ from the integrated v2 |
| `snapshots/fif-dashboard-cinematic-v4.zip` | website snapshot before the v5 fixes | 9 files differ from the current site |
| `snapshots/flame-in-freefall-kit_v4.zip`, `_v5.zip` | earlier kit snapshots | 30 / 27 files differ from the current kit |
| `snapshots/_dev_site_inputs.zip` | development snapshot of site inputs | 19 files differ from the current kit |
| `snapshots/RAG_Corpus_by_Dataset.zip` | earlier RAG export by PSI ID, generator unknown | superseded by `deliverables/rag-corpora.zip` |
| `superseded/kit-analysis-T5-PSI-20-template/` | the kit's template `data_log.md` and `findings.md` for PSI-20 | replaced by Khaled Adawi's package |

`tool-artifacts/` (another assistant's file-transfer helpers) was deleted on 15 Nov 2026 with the team's approval (logged).
Safe to delete once the team agrees: everything here. The current project does not depend on it.

- `removed/PSI-60/`: PSI-60 (SPICE ground analysis), removed from the project on 15 Nov 2026; see its README.
