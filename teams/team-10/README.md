# Team 10 "Maneno Mashinani": Kikuyu sentiment analysis (Strathmore NLP Hub Datathon 2026)

**Track:** B, sentiment (positive / negative / neutral), sentence level. **Domain:** campus cafeteria. **Language:** Kikuyu (`ki`).
**Demo video:** https://drive.google.com/file/d/1b7NWf434sJjEGYJkX0dOSmFBo4N_4ex4/view?usp=sharing

## Idea
A small Kikuyu sentiment dataset and baseline model. The model labels one sentence about the campus cafeteria as positive, negative or neutral. This is sentence-level opinion only, not emotion detection or sarcasm understanding.

## Data (`data/contribution.csv`)
- 325 Kikuyu sentences: 110 positive, 107 negative, 108 neutral. No duplicates, no blanks, no personal data.
- Method: the English source sentences were **written by an AI (Claude)** and then **translated and adapted into Kikuyu by one team member** (`source_method = human_localised`, `source_dataset = claude_generated_english_v1`). The English text is not in this repository.
- Review: a Kikuyu-speaking family member of a team member (not a team member; reviewer code `T10-R1`) reviewed a random sample of 72 rows (24 per label). Verdicts: 32 OK, 35 FIX (suggested rewording), 5 DROP. The 5 dropped rows were removed (`data/exclusion_log.csv`). In 2 FIX rows only diacritics/spacing differed, so we kept the original text. In 33 rows we adopted her rewording (typed mostly without diacritics). 67 rows are `independently_reviewed`; the other 258 are `self_reviewed`.
- Splits: random, seed 10, 205 train / 60 dev / 60 test (20 per label in dev and test). **All 60 test rows are independently reviewed**, and the unmodified `validate.py` passes.

## Approach
Character n-gram TF-IDF + logistic regression (the starter-kit baseline) against a majority-class baseline. Code: `core.py`, `train.py`, `evaluate.py`, `app.py` (Streamlit demo), `assign_splits.py`, `apply_review.py`.

## Results
| | Accuracy | Macro-F1 | Majority-baseline macro-F1 |
|---|---|---|---|
| Dev (60 rows) | 0.750 | 0.739 | 0.167 |
| Test (60 rows) | 0.683 | 0.640 | 0.167 |

Test confusion matrix (rows = true, columns = predicted; order positive, negative, neutral):
```
positive  19   0   1
negative  10   5   5
neutral    3   0  17
```
Per-label recall on test: positive 0.95, negative 0.25, neutral 0.85. The model rarely misses positive sentences but often predicts positive or neutral for true negatives (15 of 20 negatives were wrong). 19 of 60 test sentences were wrong. Full predictions: `artifacts/sentiment/test_predictions.csv`. Test was evaluated once after the settings were frozen.

### Error analysis (5 of the 19 actual test errors)
- `T10-A-014` (true negative, predicted positive)
- `T10-A-046` (true negative, predicted neutral)
- `T10-A-075` (true neutral, predicted positive)
- `T10-A-078` (true neutral, predicted positive)
- `T10-A-081` (true negative, predicted positive)

Pattern across all 19 errors: 10 negatives were predicted positive and 5 negatives neutral. We have not verified why individual sentences failed. Likely contributors are the small training set (about 68 sentences per label), a character-based model that leans on surface word pieces, and negative opinions phrased without an obvious negative word. A Kikuyu speaker should check these rows.

## Limitations (please read)
1. **Review covers only a sample.** One reviewer checked 72 of the 330 original rows. Rows outside that sample (258) are only `self_reviewed`; only 7 train/dev rows were independently reviewed. The test set is fully independently reviewed.
2. **One reviewer, one translator.** The reviewer is a single family member and not a team member; the two teammates assigned to review could not be reached. Her rewordings for 33 rows were typed mostly without diacritics (ĩ, ũ), so orthography in the data is now mixed, and we cannot confirm that every reworded sentence keeps its original label.
3. The English source sentences are AI-written, so the Kikuyu is a translation of synthetic text, not naturally occurring speech.
4. Small data (325 rows); results vary with the random split and the 60-row test set is small. No minimum score is claimed. Negative sentences are poorly detected (recall 0.25).
5. The demo's probability is uncalibrated and the model always picks one of the three labels, even for unsupported input.

## Run it
```
python -m pip install -r requirements.txt
python validate.py --track sentiment --data data/contribution.csv
python train.py    --track sentiment --data data/contribution.csv
python evaluate.py --track sentiment --data data/contribution.csv
python -m streamlit run app.py    # choose "sentiment"
```
Training writes the model to `artifacts/sentiment/model.joblib` (not committed; only load `.joblib` files you created or trust).

## Team contributions
See `CONTRIBUTIONS.md` and `docs/AI_USE_STATEMENT.md`.

## Credits and licences
Starter code from the Strathmore NLP Hub Datathon kit (MIT, see `LICENSE_CODE.txt`). AI assistance: Claude (Anthropic) wrote the English source sentences and helped with scripts and documentation; it did not write or edit the Kikuyu text. Kikuyu data: team contribution under the team's documented permission.
