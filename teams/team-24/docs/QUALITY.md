# Quality report — Team 24 (Kiswahili 5)

Kiswahili (`sw-KE`), dataset `v1`, 2026-11-11.

## Accepted contributions by source method and intent
All **262** accepted rows are `original_human` / `team_authored`. Per-intent counts are in DATA_CARD.md (every label ≥ 15 train / 5 dev / 5 test). Authors per `data/contribution.csv`: Krysia (24K) 196 rows (24-001 to 24-197); Nathan (24N) 66 rows (24-198 to 24-261, 24-372, 24-373).

## Unchanged external training rows (not counted)
**None** in the contribution. 110 rows from `Rogendo/Eng-Swa-Dataset` were excluded (no licence, no provenance, poor label fit) and were not used for training, evaluation or counts.

## Independent review counts
- **Test (52):** 43 reviewed by Moses (24M), 9 by Nathan (24N); no test row is reviewed by its recorded author. Rows 24-209 and 24-235 were first reviewed by Nathan, then re-assigned to Moses once Nathan was recorded as their author. 
- **Train/dev (210):** recorded as `independently_reviewed` by 24M on 2026-11-11, changed from `self_reviewed` on Moses's instruction; Moses attests he reviewed them. Not independently re-checked by a second person.

## Disagreements and resolutions
- Review found label/wording problems in the first batch: 7 rows were requests the 10 labels do not cover (removing a list item or calendar event, closing a list, stopping music, a travel-time question, a sleep-duration calculation). Resolved by rewording to a supported action (not forcing a label).
- 8 rows were ambiguous (no mention of a list, a timer, a vague place); reworded.
- 3 reminders relabelled `alarm_set` → `calendar_set`.
- 7 test-row concerns were raised before the test review (e.g. a future-date question labelled as current date, an alarm edit, a missing list mention); all reworded and reviewed.

## Duplicates, exclusions, missing fields
No duplicate texts after basic normalisation, no empty required fields, no email/phone patterns (validator). 110 rows excluded as above. 7 rows rewritten (see above).

## Group creation and split checks
Every row has a unique `group_id`; there are no paraphrase groups. Splits were set by hand per label. Two rows (24-094, 24-197) were moved train → test to reach 5 test rows for `calendar_set` and `play_music`. `validate.py --track intent` passes (262 records).

## Baseline and final model
Kit baseline: character n-gram (2–5) TF-IDF + logistic regression (default C=1), trained on the train split only; majority-class comparator. No settings were tuned.

| | Dev (51) | **Test (52)** |
|---|---|---|
| Accuracy | 0.824 | **0.808** |
| Macro-F1 | 0.816 | **0.790** |
| Majority-class macro-F1 | 0.021 | 0.021 |

**Per-label test F1:** alarm_set 1.000, news_query 1.000, qa_definition 1.000, play_music 0.909, datetime_query 0.800, calendar_set 0.800, weather_query 0.727, lists_createoradd 0.727, lists_query 0.600, calendar_query 0.333 (n = 5–6 each).

**Test confusion matrix** (rows = gold, columns = predicted; order: alarm_set, calendar_query, calendar_set, datetime_query, lists_createoradd, lists_query, news_query, play_music, qa_definition, weather_query):
```
alarm_set          5 0 0 0 0 0 0 0 0 0
calendar_query     0 1 2 0 0 0 0 0 0 2
calendar_set       0 0 6 0 0 0 0 0 0 0
datetime_query     0 0 1 4 0 0 0 0 0 0
lists_createoradd  0 0 0 0 4 1 0 0 0 0
lists_query        0 0 0 0 2 3 0 0 0 0
news_query         0 0 0 0 0 0 5 0 0 0
play_music         0 0 0 0 0 1 0 5 0 0
qa_definition      0 0 0 0 0 0 0 0 5 0
weather_query      0 0 0 1 0 0 0 0 0 4
```

## Five actual errors (10 of 52 test rows were wrong)
Causes below are our hypotheses from the data, not verified against model internals.
1. **24-130** *Kalenda yangu inasema nini kuhusu Jumapili?* — gold `calendar_query`, predicted `calendar_set`. Both calendar intents share words (*kalenda*, day names); the model keys on topic, not on question vs command.
2. **24-128** *Tukio langu la kwanza kesho ni lipi?* — gold `calendar_query`, predicted `weather_query`. *kesho* and a question mark are common in weather rows; the sentence has no calendar word.
3. **24-153** *Weka viazi kwenye orodha ya manunuzi ya wiki.* — gold `lists_createoradd`, predicted `lists_query`. Its ending matches a `lists_query` training row; the verb *Weka* is ignored.
4. **24-182** *Nionyeshe vilivyobaki kwenye orodha ya leo.* — gold `lists_query`, predicted `lists_createoradd`. *kwenye orodha ya* is frequent in "add to list" rows.
5. **24-209** *Washa ngoma ya zamani kwenye redio.* — gold `play_music`, predicted `lists_query`. Least certain: *redio* is unseen in training and *kwenye … ya* is a list pattern.
The other five errors (24-026, 24-050, 24-129, 24-131, 24-181) are in `artifacts/intent/test_predictions.csv`. Pattern: the model learns topic words rather than request type, so `calendar_query` (4 of 5 wrong) and the two `lists_` labels are weakest.

## Test-set use (disclosure)
- `evaluate.py` completed on the same 52 test rows several times with identical results: a first run computed scores but crashed while printing (Windows console could not encode a bar character); a re-run with UTF-8 output; and a re-run after retraining because only author/reviewer metadata changed (the data fingerprint changed). Model, text and splits were unchanged, and the scores did not change.
- The test errors were viewed **before** the cross-validation experiment below. The official result is the frozen run above.
- `train.py` and `evaluate.py` were re-run on the final submitted CSV on 2026-11-11; dev and test scores are identical to the frozen run (dev macro-F1 0.816; test accuracy 0.808, macro-F1 0.790).

## Post-hoc experiment (not the official result)
Cross-validation on train + dev only (210 rows, 5-fold × 3 repeats; test rows never loaded); 12 settings compared (`experiments/cv_compare.py`, `experiments/cv_results.json`):

| Setting | CV macro-F1 |
|---|---|
| Baseline (char 2–5, C=1) | 0.753 ± 0.049 |
| **Char 2–5, C=10** (best; better than baseline in 13/15 folds) | **0.785 ± 0.041** |
| Char + word features, C=10 | 0.779 ± 0.046 |
| Word features only, C=10 | 0.743 ± 0.061 |
| Class weights | no change (classes are balanced) |

Word features did not help. The gain is modest and slightly optimistic, because the best of 12 settings was chosen on the same data. **The improved model was not scored on the test set**, because the test set had already been viewed.

## Language variety, limits, unresolved issues
- Small dataset (5–6 test rows per label); one variety; few authors; AI-suggested wording in 35 rows (CONTRIBUTIONS.md).
- Three rows keep the loanword *alarm* by design.
- Unresolved: reviewer fluency statement, who proposed the six spreadsheet edits, release terms. All marked.
