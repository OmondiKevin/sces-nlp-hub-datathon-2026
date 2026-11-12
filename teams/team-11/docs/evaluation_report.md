# Model Evaluation Report – Team 11 Dholuo Sentiment Classification

**Team:** Team 11 – NLP Hub Datathon 2026  
**Language:** Dholuo  
**Task:** Three-class sentiment classification  
**Model:** Character-level TF-IDF with Logistic Regression  
**Report version:** Final evaluation v1.0  
**Date:** 11 November 2026  
**Status:** Final train, development and held-out test evaluation completed

## 1. Purpose

This report documents the final sentiment classification experiment using the team's 300-record contribution dataset.

The objective is to classify Dholuo text into positive, negative and neutral sentiment categories and evaluate performance on the designated development and held-out test splits.

The results are experimental. They do not establish broad linguistic validity or guarantee performance on unseen real-world Dholuo text.

## 2. Dataset and experimental setup

The final experiment used:

`data/contribution.csv`

The dataset contains 300 records, balanced across three sentiment labels:

| Label | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| **Total** | **300** |

The official dataset splits were used:

| Split | Records |
|---|---:|
| Training | 180 |
| Development | 60 |
| Test | 60 |
| **Total** | **300** |

Each split contains equal numbers of positive, negative and neutral records.

All 60 held-out test records were independently reviewed according to the dataset's review metadata.

## 3. Model configuration

The final classifier uses a character-level TF-IDF representation followed by Logistic Regression.

| Component | Configuration |
|---|---|
| Text representation | Character-level TF-IDF |
| Character n-grams | 2–5 |
| Classifier | Logistic Regression |
| Maximum iterations | 1,000 |
| Random state | 42 |
| Training data | Training split only |
| Model artefact | `artifacts/sentiment/model.joblib` |

Character n-grams were selected as a practical baseline for capturing subword patterns without requiring a large language-specific vocabulary.

The model produces class probabilities in the Streamlit demonstration. These are uncalibrated model scores and should not be interpreted as guaranteed confidence estimates.

## 4. Evaluation methodology

The final workflow was:

1. Use the final contribution CSV and official split assignments.
2. Fit the model using the training split.
3. Evaluate development performance.
4. Freeze the selected model configuration.
5. Evaluate the held-out test split once.
6. Compare results with a majority-class baseline.
7. Save test predictions and per-label evaluation results.

The test set was not used for model tuning.

## 5. Development results

The development set contained 60 examples.

| Metric | Result |
|---|---:|
| Accuracy | 70.00% |
| Macro-F1 | 0.698 |
| Majority baseline accuracy | 33.33% |
| Majority baseline macro-F1 | 0.167 |

### Development per-label results

| Label | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Positive | 0.684 | 0.650 | 0.667 | 20 |
| Negative | 0.684 | 0.650 | 0.667 | 20 |
| Neutral | 0.727 | 0.800 | 0.762 | 20 |

### Development confusion matrix

Label order: Positive, Negative, Neutral.

| Actual \ Predicted | Positive | Negative | Neutral |
|---|---:|---:|---:|
| Positive | 13 | 3 | 4 |
| Negative | 5 | 13 | 2 |
| Neutral | 1 | 3 | 16 |

The development results show stronger performance on neutral examples than on positive and negative examples.

## 6. Final held-out test results

The held-out test set contained 60 examples, with 20 examples per sentiment class.

<badge color="success">Final test evaluation completed</badge>

| Metric | Result |
|---|---:|
| Test accuracy | 61.67% |
| Test macro-F1 | 0.611 |
| Majority baseline accuracy | 33.33% |
| Majority baseline macro-F1 | 0.167 |

### Test per-label F1

| Label | F1-score | Support |
|---|---:|---:|
| Positive | 0.651 | 20 |
| Negative | 0.500 | 20 |
| Neutral | 0.683 | 20 |

The model outperformed the majority-class baseline on the held-out test set.

However, test performance was lower than development performance. Negative sentiment was the weakest class, with an F1-score of 0.500.

The difference between development and test results should be treated as a limitation of the current small evaluation sample, not as evidence of general performance.

## 7. Error analysis

The final evaluation outputs include:

- `artifacts/sentiment/test_predictions.csv`
- `artifacts/sentiment/per_label_report.csv`
- `artifacts/sentiment/test_metrics.json`

These files preserve the held-out test predictions and evaluation results.

Negative sentiment had the lowest test F1-score. Further investigation should examine errors involving negation, idiomatic expressions, ambiguous sentiment and contextual meaning.

Any linguistic interpretation of individual errors should be checked by a proficient Dholuo speaker. No unsupported explanation of a model error should be treated as established.

## 8. Baseline comparison

The majority-class baseline predicts the most frequent training label for every example.

Because the training data are balanced, the baseline achieves:

| Metric | Majority baseline |
|---|---:|
| Test accuracy | 33.33% |
| Test macro-F1 | 0.167 |

The final model achieved 61.67% test accuracy and 0.611 macro-F1, outperforming this simple baseline.

## 9. Limitations

1. The dataset contains only 300 records and is small relative to the diversity of Dholuo.
2. All records derive from Sindhi source material. Google Translate produced the initial Dholuo drafts for all 300 records; 276 were used largely as translated, while 24 were subsequently human-localised.
3. Broader linguistic validation by proficient Dholuo speakers remains necessary.
4. The dataset may not represent all dialects, speakers or conversational contexts.
5. Character-level TF-IDF may not capture deeper semantic and cultural meaning.
6. Negation, idioms, sarcasm, mixed sentiment and code-switching may be difficult to classify.
7. Negative sentiment had the weakest held-out test F1-score.
8. Predicted probabilities are not calibrated confidence estimates.
9. Source provenance and redistribution rights still require review.

The results should therefore be presented as experimental performance on this specific contribution dataset, not as a validated measure of general Dholuo sentiment understanding.

## 10. Reproducibility

The final experiment can be reproduced using the supplied scripts and dataset, subject to the availability and permission to use the dataset.

Install the project dependencies, then run:

```powershell
python train.py --data data/contribution.csv --track sentiment
python evaluate.py --data data/contribution.csv --track sentiment
```

Relevant files:

| File | Purpose |
|---|---|
| `data/contribution.csv` | Final contribution dataset |
| `train.py` | Training pipeline |
| `evaluate.py` | Held-out evaluation |
| `artifacts/sentiment/model.joblib` | Trained model |
| `artifacts/sentiment/dev_metrics.json` | Development metrics |
| `artifacts/sentiment/test_metrics.json` | Test metrics |
| `artifacts/sentiment/test_predictions.csv` | Test predictions |
| `artifacts/sentiment/per_label_report.csv` | Per-label test report |

The model configuration uses random state 42. The evaluation script checks the dataset fingerprint to ensure that the model corresponds to the dataset used for evaluation.

## 11. Conclusion

The team trained and evaluated a character-level TF-IDF and Logistic Regression classifier using the final 300-record contribution dataset.

The model achieved 70.00% development accuracy and 69.8% development macro-F1. On the held-out test set, it achieved 61.67% accuracy and 0.611 macro-F1, outperforming the majority baseline macro-F1 of 0.167.

The test results are more modest than the development results, and negative sentiment remains the weakest class. These findings should be reported transparently alongside the dataset's linguistic and provenance limitations.

**Report status:** Final model evaluation completed; broader linguistic validation and source-rights review remain outstanding.

## Confusion matrix

Rows represent actual labels; columns represent predicted labels. Label order: negative, neutral, positive.

| Actual / Predicted | Negative | Neutral | Positive |
|---|---:|---:|---:|
| Negative | 9 | 5 | 6 |
| Neutral | 3 | 14 | 3 |
| Positive | 4 | 2 | 14 |

The model correctly classified 37 of 60 test records (61.7%). Negative sentiment was the weakest class, with 9 of 20 correctly classified. These results are experimental and do not establish generalisable Dholuo sentiment performance.

