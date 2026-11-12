# DATA_PLAN.md

Strathmore NLP Hub Datathon 2026

## 1. Team and task

| Field | Value |
|---|---|
| Team number | 1 |
| Track | B: sentiment analysis |
| Language | Kamba (ISO 639-3: kam), language code in data: `kam-KE` |
| Kamba variety | [TO CONFIRM at Meeting 1, for example Machakos or Kitui Kamba. Set by Member 3.] |
| Labels | `positive`, `negative`, `neutral` |
| Unit of annotation | One sentence, one declared target |
| Plan date | Saturday 7 November 2026 |
| Final submission deadline | Wednesday 11 November 2026, 11:59 p.m. EAT |

**Status of this file:** committed before any Kamba data was written. Items marked TO CONFIRM are decided at Meeting 1 and recorded here by committing an updated version.

## 2. Domain and target

- **Domain:** campus Wi-Fi feedback. [TO CONFIRM at Meeting 1. If the team changes domain, edit this line and commit before writing data.]
- **Target of opinion:** the campus Wi-Fi service (for example its speed, reliability, coverage, or the support received).
- Every sentence is labelled only for the opinion it expresses toward this target. One domain and one target for the whole dataset.

## 3. Source method

- **source_method:** `original_human`.
- **source_dataset:** `team_authored`, **source_version:** `v1`, **source_url:** `not_applicable`.
- **licence_or_permission:** `documented_contributor_permission`. Each author gives written permission for the sentences to be used in the datathon and the NLP Hub review. The evidence is kept in a private folder, not in the public repository.
- Kamba is not covered by AfriSenti. No external dataset is used and none counts toward the contribution target.
- All sentences are written by Kamba speakers on the team. We do not use machine translation. We do not use AI to generate sentences. AI may be used for code and explanations only and will be declared in the contribution and AI-use statement.
- Sentences contain no names, phone numbers, admission numbers or other personal details.

## 4. Labels and annotation rules

| Label | Use when |
|---|---|
| `positive` | The sentence expresses approval of the target. |
| `negative` | The sentence expresses disapproval of the target. |
| `neutral` | The sentence states a fact or asks something without a clear opinion. |

Rules (details in the annotation guide):
- Read the whole sentence. Negation can reverse meaning. Do not label from one favourable or unfavourable word.
- Exclude mixed opinion, sarcasm and unclear targets. Record each one in the Exclusion Log with a reason.
- Include on purpose: minimal pairs (same words, opposite label), negation, neutral sentences that contain evaluative words, and opinions with no obvious sentiment word.
- Vary length, word order and vocabulary. Do not create data by swapping one word or name in a template.
- Keep original spelling and diacritics. Record real code-switching (Swahili or English) in the `code_switching` column.

## 5. Dataset size and splits

| Label | Train | Dev | Test | Total |
|---|---|---|---|---|
| positive | 60 | 20 | 20 | 100 |
| negative | 60 | 20 | 20 | 100 |
| neutral | 60 | 20 | 20 | 100 |
| **Total** | 180 | 60 | 60 | **300** |

- Minimum is 300 accepted records. We aim for a few extra so weak records can be dropped during review.
- **Grouping:** minimal pairs, paraphrases and sentences built from the same idea share a `group_id` and stay in one split. A group is never split across train, dev and test.
- Test data is used once, after the model, data and settings are frozen.

## 6. Authorship and review plan

| Member | Role | Code | Writes | Reviews |
|---|---|---|---|---|
| Member 1 (Ian) | Data Documentation Lead | T01-A | About 100 records, including 30 test records | Documents and counts |
| Member 2 | Code | T01-B | About 100 records, including 30 test records | Code and demo |
| Member 3 | Language Review | T01-C | About 100 records, train and dev only | All 60 test records, and at least 20 percent of other train and dev records |

- Every test record is independently reviewed. `reviewer_code` must differ from `contributor_code`.
- Member 3 writes no test records, so that they can review the whole test set independently.
- Disagreements and corrections are recorded in the Review Log with the original value, the corrected value and the reason.
- **Assumption to confirm at Meeting 1:** only Member 3 is confirmed fluent in Kamba. If another member is not fluent they do not author or review Kamba text. Ask the organisers or mentor for a second fluent reviewer if needed.

## 7. Source log

- **File:** `Kamba_Source_Log.xlsx`, kept in the team repository under `data/` (cleared data only; no private evidence).
- **One row per accepted sentence.** It records: `record_id`, `text`, `label`, `contributor_code`, `reviewer_code`, `review_status`, `group_id`, `split`, `variant` (original, minimal_pair, paraphrase, translation), `adjudication_note`, plus `english_gloss` and `code_switching` as helper columns.
- **Constant fields** (`language`, `source_dataset`, `source_version`, `source_record_id`, `source_url`, `source_method`, `licence_or_permission`) fill from the Settings sheet.
- **Record IDs:** `T01-<letter>-<number>` (for example `T01-A-001`). Each member numbers their own records.
- **Companion sheets:** Groups (keeps related sentences together), Tally (counts against targets), Exclusion Log, Review Log.
- **Export:** columns A to Q only, saved as UTF-8 CSV to `data/contribution.csv` after the data freeze. No `pending_review` rows in the export.

## 8. Dates and meetings

| Date (EAT) | Milestone |
|---|---|
| Sat 7 Nov | Repo, DATA_PLAN.md, annotation guide v0, 30-sample set. Meetings 1 (5:00 pm) and 2 (9:00 pm). |
| Sun 8 Nov | Bulk writing, test review starts. Meeting 3 (8:00 pm). |
| Mon 9 Nov | Data complete, test review finished. Meeting 4 (1:00 pm). Data freeze at Meeting 5 (9:00 pm). |
| Tue 10 Nov | Dev experiments, one final test run, demo, documents. Meetings 6 (2:00 pm) and 7 (8:00 pm). |
| Wed 11 Nov | Tag `submission-v1`, record the full commit SHA, make the ZIP, submit. Meeting 8 (10:00 am). |

## 9. Quality and integrity commitments

- No practice rows count as contribution. No unchanged downloads are used.
- Test data is not used for tuning. Dev results are never reported as test results. No scores are invented.
- Disputed or unclear-rights records are quarantined and noted, not hidden.
- The demo uses the trained model on new input. It states the detected opinion and shows an uncalibrated probability. It does not answer the text.
- The model is evaluated against a majority-class baseline. A separate challenge set (negation, neutral sentences with evaluative words, opinions without obvious sentiment words) is reported separately and never used for training.

## 10. Open decisions (fill in at Meeting 1)

- [ ] Domain and target confirmed: campus Wi-Fi feedback / other: ________
- [ ] Kamba variety: ________
- [ ] Who is fluent in Kamba, and any second reviewer: ________
- [ ] Where the meetings take place (call or in person): ________
- [ ] Private permission evidence folder location (not in the repo): ________

## 11. Attribution

Built from the Strathmore NLP Datathon 2026 Starter Kit v2.0 and handbook. The Kamba data is the team's own work.
