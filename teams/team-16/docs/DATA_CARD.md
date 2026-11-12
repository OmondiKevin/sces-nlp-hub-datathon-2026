# Dataset card: Team 16 Kinyarwanda sentiment

**Working version:** 1.3  
**Snapshot date:** 10 November 2026  
**Primary file:** `data/contribution.csv`  
**Task:** Sentiment Analysis

## Summary

The file contains 345 Kinyarwanda examples labelled `positive`, `negative`, or `neutral`. It is intended for the Strathmore NLP Datathon 2026 as part of Team 16 Kinyarwanda's work.

## Composition

| Source method recorded in CSV | Count | Current use |
|---|---:|---|
| `original_human` | 30 | Train/dev/test |
| `human_localised` | 199 | Train/dev/test |
| `llm_generated` | 116 | Train only |
| **Total** | **345** | |



## Labels and split counts

| Label | Train | Test | Dev | Total |
|---|---:|---:|---:|---:|
| Negative | 69 | 23 | 23 | 115 |
| Positive | 69 | 23 | 20 | 112 |
| Neutral | 69 | 23 | 26 | 118 |

All `llm_generated` rows are in training, consistent with the organizer's instruction that synthetic data must not be used in dev or test. The split was balanced before a native reviewer corrected five labels; those corrections changed the current class totals and dev distribution. Test contains 69 examples, 23 per label.

## Collection and review

The CSV marks all 345 rows `independently_reviewed` by `reviewer_001`. The project plan maps that code to `Innocent Mukiza`, a native Kinyarwanda speaker.

## Intended uses and limits

- Suitable for a small sentiment-analysis experiment on short Kinyarwanda text.
- Not evidence of performance across all dialects, regions, ages, registers, or code-switched text. Dialect, demographic, and domain metadata are not collected.
- The reviewer noted that several examples use a formal written register. 
- Neutral sentiment is difficult when a factual outcome is mildly favorable or unfavorable. 
- The dataset is small and includes 116 synthetic training records. Results may be sensitive to wording overlap, source style, and label decisions.
- Text is intended to be privacy-safe. `validate.py` checks for common email and phone patterns, but that check is not a guarantee that all identifying information has been removed.

## Processing and quality checks

Text is stored in UTF-8. The project validator checks required fields, unique IDs, normalized duplicate text, allowed labels/splits, group-to-split consistency, common phone/email patterns, and minimum per-label counts. A structural inspection on 10 November 2026 found 345 rows, no blank fields, unique IDs, no normalized duplicate sentences, no group IDs spanning splits, and no synthetic rows outside train. 

The current `group_id` values are broad label/split buckets (for example, `group_neg_train`).

## Model and reporting status

`train.py` specifies character TF-IDF features (2–5 character n-grams), a `LinearSVC`, and a most-frequent-label baseline. `artifacts/dev_metrics.json` reports an earlier 69-example dev result (accuracy 0.710, macro-F1 0.711; majority baseline accuracy 0.333, macro-F1 0.167). Its per-label support is 23 each, which does not match the current dev counts after the five label corrections. Treat those metrics as stale; retrain and recompute before reporting. No current frozen-test metrics are recorded in this card.