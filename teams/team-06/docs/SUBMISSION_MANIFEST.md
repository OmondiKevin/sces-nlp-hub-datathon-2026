# Submission Manifest — Team 6

| Item | Value |
|---|---|
| Team | 6 — Data Buddies |
| Primary language | Luganda |
| Track | A — Intent classification |
| GitHub URL | https://github.com/syd-xo/DataBuddies.git |
| Frozen commit SHA | `52b0deb52806f8b681d7dd2aaa99744d7c815b13` |
| Tag | `submission-v1` |
| Data counts | 250 total; 150 train / 50 dev / 50 test; 25 per intent |
| Source licence/permission | Code: MIT (`LICENSE_CODE.txt`); Data: `documented_contributor_permission` (private evidence, see `SOURCE_LOG.md`) |
| Metric files | `artifacts/intent/test_metrics.json`, `artifacts/intent/per_label_report.csv`, `artifacts/intent/test_predictions.csv` |
| Demo run instructions | `python mobile_app.py` (see `README.md`); open `http://127.0.0.1:8501` in a browser |
| Demo recording | `https://youtu.be/PAHOlETQBy0` |
| Known unresolved issues | `LG-LIS-023_2` label boundary may be arguable (see `docs/QUALITY.md` §4, row 4); left unchanged. No other unresolved issues. |
| ZIP snapshot | `Team06-DataBuddies-submission-v1.zip` (downloaded from the `submission-v1` tag on GitHub)  |

## Pre-submission checklist
- [ ] `data/contribution.csv` validated (`PASS: 250 records`).
- [ ] All 250 rows: `review_status = independently_reviewed`, `reviewer_code = REV-LG-2026`.
- [ ] `evidence/REVIEW_LOG.csv` present.
- [ ] All eight `.md` documents present and complete.
- [ ] `artifacts/intent/*` populated from a frozen model.
- [ ] `QUALITY.md` metrics and error table pasted from real artifacts.
- [ ] README results section matches `QUALITY.md`.
- [ ] Demo recording uploaded and linked.
- [ ] Commit tagged `submission-v1`, SHA captured, ZIP downloaded.
- [ ] Pull request opened against `OmondiKevin/sces-nlp-hub-datathon-2026`, targeting `teams/team-06/`, titled `Team 06 | Final submission`, before the deadline.