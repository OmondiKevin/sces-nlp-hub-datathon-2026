# Team 14 (Maa): Strathmore NLP Hub Datathon 2026

Track A, intent classification for **Maasai (Maa, `mas`)**.

- Original team repository (private): https://github.com/Philtait/nlp-datathon-2026-team-14
- Source commit (full SHA): `PASTE_FULL_SHA_HERE` (tag `submission-v1`)
- Demo and presentation video: https://drive.google.com/file/d/1LjqFfroIyVRxdCI1kincDOl8eIYMhW_B/view?usp=drive_link
- Source commit: the commit tagged `submission-v1` in this repository. Its full SHA is in the submission copy of this README.

## 1. Team and project

**Members and contributions.** We split the work by assigning GitHub issues.

| Member | Issues | What that covered |
|---|---|---|
| Philip Tait | #1, #2, #4, #16, #18 | Starter kit, data plan, Google Form and data collection, contribution statement, freezing and submitting. Also set up the repo, board and milestones and approved pull requests. |
| Neema Mapelu Naserian | #3, #5, #6, #7, #8, #14, #15 | Annotation guide, cleaning, groups and splits, worked with the reviewer (R01) and logged the review, built `data/contribution.csv`, dataset card, quality report. |
| Mayabi Muigai Ivan | #9, #10, #11, #12, #13, #17 | Baseline training and evaluation, error analysis, Streamlit demo, demo recording, README. |

Details and evidence are in `docs/CONTRIBUTIONS.md`. R01 is an outside reviewer, not a team member (see section 2).

**Idea.** Phone assistants rarely understand Maa. We built a small reviewed dataset of everyday requests in Maa and a baseline model that predicts what the user wants (weather, time, alarm, calendar, lists, music, news, word meanings). The intended users are Maa speakers who would talk to a phone assistant in their own language. The demo shows a simulated response only and does not perform any real action.

**Approach**
1. Collected requests with a Google Form: 20 everyday situations in English, and speakers wrote what they would say in Maa.
2. An outside native Maa speaker (R01) reviewed the raw export, then the text was normalised and duplicates and unusable answers were removed (1,247 answers down to 1,024 records).
3. Validated the data and split it into 687 train, 172 dev and 165 test records.
4. Trained the starter-kit baseline (character 2 to 5-gram TF-IDF with logistic regression), used dev to check it, and evaluated test.
5. Built a Streamlit demo that runs the trained model on new input.

**Language and variety.** Contributors come from several Maa-speaking communities. The largest groups are Kaputiei (10 contributors) and Kajiado (5), and 5 did not name one (`docs/DATA_CARD.md`). We do not claim one standard variety. R01 speaks the Illukumae variety.

## 2. Data and review

- **Records:** 1,024, all `original_human`. Train 687, dev 172, test 165. Language code `mas`.
- **Per label (all splits):** weather_query 107, datetime_query 99, alarm_set 116, calendar_set 103, calendar_query 109, lists_createoradd 100, lists_query 97, play_music 90, news_query 100, qa_definition 103.
- **Contributors:** 41 Maa speakers (codes C01 to C41), credited by code only. 29 said Maa is their first language or that they speak it fluently, 8 use it comfortably every day, and 4 know some Maa but are not confident. R01 reviewed all their answers.
- **Collection:** form open 9 to 11 November 2026. A few responses arrived after the review, cleaning and training and are not in the dataset.
- **Review:** R01, a native Maa speaker (Illukumae variety, Narok County), reviewed all 1,247 raw answers. R01 corrected 124 and deleted 136, and changed no labels. R01 did not fill in the form. **R01 is a relative of a team member, and nobody checked R01's review.** The review was done on the raw export before record IDs existed, so decisions are logged by count (`docs/review_log.md`).
- **Splits:** `group_id` is contributor plus intent, so the same contributor can appear in more than one split. 33 of 41 contributors appear in both train and test, and all 41 appear in more than one split (`docs/splits.md`).
- **Reused vs contributed:** we reused the organiser starter kit v2.0 code (`validate.py`, `train.py`, `evaluate.py`, `core.py`, MIT licence). We contributed the Maa dataset, the documents and the changes to `app.py`. The practice CSVs in `data/` are teaching examples and count as zero contribution. The cleaning script (`clean_responses.py`) is kept outside the repository because it handles Maa text, so it is not included.
- **Links:** `data/contribution.csv`, `docs/DATA_PLAN.md`, `docs/ANNOTATION_GUIDE.md`, `docs/DATA_CARD.md`, `docs/QUALITY.md`, `docs/cleaning_summary.md`, `docs/review_log.md`, `docs/splits.md`, `docs/CONTRIBUTIONS.md`.

## 3. Install, run and reproduce

Python 3.10 or later. Dependencies are pinned in `requirements.txt` (scikit-learn, pandas, streamlit, joblib).

```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate.py --track intent --data data/contribution.csv
python train.py --track intent --data data/contribution.csv
python -m streamlit run app.py
```

`model.joblib` is not in the repository (it is gitignored), so run `train.py` before the demo. `train.py` overwrites `artifacts/intent/dev_metrics.json`.

The test set was evaluated by one official run of `evaluate.py`. Running it again overwrites `artifacts/intent/test_*` files, so do it in a separate copy:

```
python evaluate.py --track intent --data data/contribution.csv
```

## 4. Results

Model: character 2 to 5-gram TF-IDF with logistic regression (the unchanged starter-kit baseline), compared with a majority-class baseline. All figures come from `artifacts/intent/`.

| Metric | Dev (172) | Test (165) |
|---|---|---|
| Accuracy | 0.901 | 0.909 |
| Macro-F1 | 0.897 | 0.906 |
| Majority baseline macro-F1 | not reported | 0.020 |

Test F1 per label: weather_query 1.000, datetime_query 1.000, play_music 1.000, news_query 0.970, qa_definition 0.938, alarm_set 0.923, calendar_query 0.867, calendar_set 0.839, lists_createoradd 0.811, lists_query 0.714.

Files: `artifacts/intent/test_metrics.json`, `dev_metrics.json`, `per_label_report.csv`, `confusion_matrix.csv`, `test_predictions.csv`.

**Note on the test set.** Before the official run, an AI tool ran the same baseline once on the cleaned file as a sanity check, and it also printed the test score (0.906). Nothing was changed after seeing it. See `docs/CONTRIBUTIONS.md`.

**Errors.** 15 of 165 test records were misclassified. The largest group is `lists_query` predicted as `lists_createoradd` (6 of 15). Real examples with record IDs are in `docs/error_analysis.md` and `docs/QUALITY.md`. A likely cause is that the word separating the two list requests is short and carries little weight in character n-grams. We have not tested this.

## 5. Limitations and known issues

- Contributors overlap across splits (33 of 41 are in both train and test), and every contributor answered the same 20 situations. The 0.909 test accuracy is probably optimistic.
- One reviewer checked all answers, is related to a team member, and was not checked by anyone. R01's spelling choices may not match other communities' conventions. Review decisions are logged by count, not by record.
- Four contributors said they are not confident in Maa. Their answers were kept after R01's review.
- Nineteen answers were excluded after the review, on the basis of sentence structure and not Maa knowledge (see `docs/cleaning_summary.md`).
- The data is written text, not transcribed speech, and orthography varies between speakers.
- The model always picks one of the 10 labels, even for unsupported input, and its probability is not calibrated.
- English glosses of Maa words in the demo and error analysis are approximate and no Maa speaker has checked them.
- The `licence_or_permission` field in the CSV says CC-BY-4.0. The form's consent notice covered use in the datathon and possible NLP Hub review, credited by code. We are confirming with the organisers that this is sufficient. Release terms are pending.

## 6. AI use, licensing and credits

- **Neema:** Claude Code (Anthropic), 5 to 11 November 2026: run guide, counting the reviewer's changes, the cleaning script, 19 suggested exclusions, setting the review fields, a sanity run of the baseline, drafting documents, and making her branches and pull requests (#21 to #27) on her account.
- **Ivan:** Gemini and Claude, while building the demo and README. Some AI output left citation markers in `app.py`, which we removed.
- **Philip:** Claude (claude.ai), 9 to 12 November 2026, for planning, workflow guides, the form structure, packaging and document drafts; Claude Code on 12 November to check the repo against the submission checklist.
- No AI tool wrote, translated, corrected or labelled any Maa text. Full statement: `docs/CONTRIBUTIONS.md`.
- Code: organiser starter kit under the MIT licence (`LICENSE_CODE.txt`). Dataset terms are pending (see section 5). Raw form responses, consent records and contributor details are private and not in this repository.