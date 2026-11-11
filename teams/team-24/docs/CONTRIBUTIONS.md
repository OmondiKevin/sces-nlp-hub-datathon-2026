# Contributions and AI use — Team 24 (Kiswahili 5)

Contributor codes are pseudonymous: 24M = Moses, 24K = Krysia, 24N = Nathan.

## Member contributions
| Member | Contribution | Evidence |
|---|---|---|
| Moses (24M) | Reviewed 43 of 52 test rows; recorded as reviewer of the train/dev rows on 2026-11-11 (attested by Moses); directed the label/wording fixes; set up the repo; ran validation, training and evaluation with AI assistance. 

| Krysia (24K) | Wrote 196 team-authored rows: 24-001 to 24-197. | `contributor_code` in the CSV |

| Nathan (24N) | Wrote 66 team-authored rows: 24-198 to 24-261 (64 rows) and 24-372, 24-373; reviewed 9 test rows (052, 077, 078, 105, 127, 157, 179, 180, 181). An initial batch of 110 rows recorded under 24N from an external source was excluded (licence/provenance). | `contributor_code`, `reviewer_code` |

## Upstream datasets and code reused
- Organiser starter kit v2.0: `validate.py`, `train.py`, `evaluate.py`, `app.py`, `core.py`, templates (code licence: `LICENSE_CODE.txt`). Credited in README.
- Libraries per `requirements.txt` (scikit-learn, pandas, streamlit, joblib).
- Label schema from the organiser's MASSIVE-aligned taxonomy. No MASSIVE, AfriSenti or Common Voice rows are in the contribution.
- Excluded, not used: `Rogendo/Eng-Swa-Dataset` (no licence). See DATA_CARD.md.

## AI tools used, dates, purpose and affected files
**Claude (Anthropic), via Claude Code, 2026-11-06 to 2026-11-11.**
- Read the handbook and starter kit; explained the task.
- **Suggested replacement wording** that the team approved, for **21 distinct rows**: 24-032, 24-037, 24-077, 24-105, 24-142, 24-157, 24-209 (first batch); 24-022, 24-056, 24-158, 24-159, 24-160, 24-161, 24-178, 24-179 (second batch); 24-052, 24-078, 24-127, 24-180, 24-181, 24-235 (third batch, plus 24-077 again).
- Applied the mechanical changes (3 relabels, 2 train→test moves) and ran validation

## Human checks applied
- Validator passes on the final CSV; model results were produced by the organiser's scripts and re-run to confirm.
- Teammates' later spreadsheet edits to five test rows the model had misclassified were not merged (see QUALITY.md).

## Generated suggestions rejected
- A proposal to evaluate the improved model on the test set was declined; only cross-validation on train/dev is reported.

## Statement
No AI-generated labels were generated and counted as independently validated human data. This exercise does not by itself create any claim to paper authorship.
