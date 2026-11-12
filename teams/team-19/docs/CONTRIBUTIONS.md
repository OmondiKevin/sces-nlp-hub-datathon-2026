# Contributions and AI use

| Member | Contribution | Evidence |
|---|---|---|
| Harry Sigei (T19-A) | data lead, wrote and rewrote sentences, training, evaluation, demo | data/source/ spreadsheets, data/review_changes.csv, results/ |
| Ezra Ntwiga (T19-EN) | independent review of the 50 test sentences | reviewer_code on test rows in data/contribution.csv |
| Michael Majau | wrote dataset sentences, rewrote flagged rows | data/source/ spreadsheets |

**Upstream code reused:** Strathmore NLP Hub Datathon 2026 starter kit (validate.py, train.py, evaluate.py, core.py, app.py).

**AI tools used:** Claude (Anthropic, model Claude Opus 5.5), 11–12 Nov 2026, used to:
- review the draft dataset and flag records whose text did not match their label, duplicates, empty rows, typos and paste artefacts;
- write per-row reasons and fix instructions for the 83 rows the team then rewrote themselves (`data/review_changes.csv`, review_reason column);
- write the build/packaging scripts `team19_final.py` and `team19_package.py` and the team instruction sheet;
- draft this documentation and README structure.

AI did not write any dataset sentence. All 250 sentences were written by team members.

**Human checks applied:** Harry and Michael rewrote every flagged row themselves; Ezra independently reviewed the test split; the starter-kit validator checks fields, duplicates, splits and review status.

No AI-generated text or labels are counted as independently validated human data.
