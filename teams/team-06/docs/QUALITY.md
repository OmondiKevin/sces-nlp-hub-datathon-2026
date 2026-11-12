# Quality and Evaluation Report — Team 6

## 1. Checks performed
- **Automated:** `python validate.py --track intent --data data/contribution.csv`
  → `PASS: 250 records; language quality, permission and semantic duplicate review remain human responsibilities.`
- **Manual review:** every row reviewed by `REV-LG-2026`; 100% of test rows independently reviewed. Reviewer codes are pseudonymous and the reviewer is not the author of any row they reviewed.
- **Split integrity:** 150 train / 50 dev / 50 test; 15 / 5 / 5 per intent; the 50 test rows were held back and never used for training or tuning.
- **Duplicate-text check:** 0 duplicated `text` values.

## 2. Review, disagreements and exclusions
No records were excluded. All 250 candidate records were accepted after review; per-row reviewer decisions (text, label, notes) are recorded in `evidence/REVIEW_LOG.csv`.

**One label flagged post-hoc:** `LG-LIS-023_2` was accepted as `lists_query` at review time, but post-evaluation analysis found the boundary arguable (see §4, row 4). Left unchanged in the test set.

**Data-cleaning decisions:**
- 50 duplicated `record_id` values were resolved by suffixing `_2` on the second occurrence (see `DATA_PLAN.md`). Text and labels unchanged.
- No spellings were normalised; original Luganda apostrophes and diacritics preserved.

## 3. Metrics (test set, frozen model — from `artifacts/intent/test_metrics.json`)

| Metric | Model | Majority baseline |
|---|---|---|
| Accuracy | **0.90** | 0.10 |
| Macro-F1 | **0.8992** | 0.0182 |
| Test size | 50 (5 per intent) | 50 |

**Why the majority baseline is 0.10:** the test set is exactly balanced (5 per intent), so there is no true majority class. The baseline classifier breaks the tie by predicting the alphabetically first label (`alarm_set`) for every row. It matches all 5 `alarm_set` examples (accuracy 5/50 = 0.10) and misses all other 45. The trained model's macro-F1 is roughly **49×** the baseline.

### Per-label results (`artifacts/intent/per_label_report.csv`)

| Label | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| weather_query | 1.000 | 0.800 | 0.889 | 5 |
| datetime_query | 1.000 | 0.800 | 0.889 | 5 |
| alarm_set | 1.000 | 1.000 | 1.000 | 5 |
| calendar_set | 0.833 | 1.000 | 0.909 | 5 |
| calendar_query | 1.000 | 0.800 | 0.889 | 5 |
| lists_createoradd | 0.714 | 1.000 | 0.833 | 5 |
| lists_query | 1.000 | 0.600 | **0.750** | 5 |
| play_music | 1.000 | 1.000 | 1.000 | 5 |
| news_query | 0.714 | 1.000 | 0.833 | 5 |
| qa_definition | 1.000 | 1.000 | 1.000 | 5 |

Three labels reach F1 = 1.00 (`alarm_set`, `play_music`, `qa_definition`). The weakest label is `lists_query` (F1 = 0.750), which loses 2 of its 5 test examples to `lists_createoradd`. `calendar_set` and `news_query` lose precision (0.833, 0.714) by attracting false positives from their sibling labels.

### Confusion matrix (from `test_metrics.json`)
| Expected → Predicted | Count |
|---|---|
| `weather_query` → `news_query` | 1 |
| `datetime_query` → `news_query` | 1 |
| `calendar_query` → `calendar_set` | 1 |
| `lists_query` → `lists_createoradd` | 2 |
| All other expected labels | 5 / 5 correct |

**Most-confused pairs:**
1. **`lists_query` ↔ `lists_createoradd` (2 errors, weakest label)** — both share the Luganda noun `olukalala` (list). Character n-grams from that shared root dominate the TF-IDF signal, and the classifier collapses them into the "create/add" verb-pattern rather than reading the `biki` ("what") / `kola` ("make") distinction.
2. **`weather_query` and `datetime_query` → `news_query` (1+1 errors)** — all three are "tell me something" information requests; the model cannot separate them from surface form alone.
3. **`calendar_query` → `calendar_set` (1 error)** — both share the root `kalenda`; the verb that distinguishes them is masked by the shared noun's character n-grams.

## 4. Error analysis (all 5 real test errors)

> Every row below is copied verbatim from `artifacts/intent/test_predictions.csv`.
> Explanations and probabilities match the diagnostics in `mobile_app.py`, which
> can be reproduced by running `python mobile_app.py` and clicking any error row.
> The model made exactly five errors on the 50-row test set.

| # | Record ID | Input (Luganda) | Expected | Predicted | Likely cause |
|---|---|---|---|---|---|
| 1 | `LG-WEA-021` | Waliwo okulabula ku mazzi ag'ennyandagala leero? | `weather_query` | `news_query` | Rare words (`okulabula`, `ennyandagala`) gave little weather evidence. Strongest n-grams were `ag'` and `ul`, which the model links to news. Probability 0.11 (correct) vs 0.15 (`news_query`) — near coin-flip. |
| 2 | `LG-DAT-024` | Mbuuliraessaawa z'omu kitundu kino. | `datetime_query` | `news_query` | `Mbuulira` ("tell me") also opens news requests; the model keyed on `buul` / `lir` and underweighted `essaawa` (time), which is rare in training. The missing space in `Mbuuliraessaawa` compounds the error. |
| 3 | `LG-CAL-022_2` | Olukungaana lw'essaawe nnya mu makya lucyali ku kalenda? | `calendar_query` | `calendar_set` | Both calendar intents share `kalenda`; the cue `lucyali ku kalenda` (is it still there?) is subtle for a character model. Probability 0.22 (`calendar_set`, chosen) vs 0.19 (`calendar_query`, correct). |
| 4 | `LG-LIS-023_2` | Esukaali yongereddwa ku lukalala lw'ebiyingira? | `lists_query` | `lists_createoradd` | Shared root `olukalala`; `yongereddwa` ("was added") triggered the "add" class. **Label may be arguable** — sentence reads as both statement and question. Flagged for a second reviewer. |
| 5 | `LG-LIS-024_2` | Laga olukalala lw'abagenyi b'olukungaana. | `lists_query` | `lists_createoradd` | `Laga` ("show") is the only cue for reading a list and is rare in training. `olukalala` is shared by both list intents, so the model fell back on add-to-list: 0.21 (`lists_createoradd`) vs 0.17 (`lists_query`). |

## 5. Limitations
- **Small test set:** 5 examples per label. Each per-label F1 is a 5-item estimate; one flipped prediction moves F1 by ~0.05–0.10. Do not compare raw scores across teams or languages.
- **Surface model:** Character-level TF-IDF (n-grams 2-5) + Logistic Regression. Cannot learn morphology or intent-level semantics; the five observed errors are all in the class of "shared surface word, different intent."
- **Uncalibrated probabilities:** the confidence shown in the app is not calibrated and must not be read as a correctness probability.
- **No abstention:** the app always returns one of the ten labels, even for unsupported input.
- **Scope:** one authored data set in one Luganda variety; no claim of cross-variety or cross-domain generalisation.

## 6. Validator is not quality proof
The structural validator checks column presence, split sizes and ID uniqueness. It cannot judge Luganda fluency, label correctness, or permission. Those were verified by the human reviewer and the author, and documented above and in `SOURCE_LOG.md`.