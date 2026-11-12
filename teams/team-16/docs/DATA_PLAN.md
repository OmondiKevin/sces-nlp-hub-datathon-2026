# Data plan

## Team 16 / Kinyarwanda / sentence-level sentiment

- **Native-language reviewer:** Innocent Mukiza (`reviewer_001`), a native Kinyarwanda speaker and non-member friend, as recorded in the original plan. Confirm his capacity and completed review scope with him.
- **Data plan:** The working file is `data/contribution.csv`. It contains original human-authored, human-localised, and synthetic records. Synthetic records are restricted to training and should be used only if available data is inadequate.
- **Record target:** At least 300 accepted contribution records. The current file contains 345 rows, but the organizer did not explicitly answer whether external dataset rows count toward 300. Treat the target as team-created contributions unless the organizer clarifies otherwise.
- **External data:** On 10 November 2026, the organizer confirmed that AfriSenti's Kinyarwanda subset may be used for sentiment analysis. No AfriSenti rows are identified in `contribution.csv`. The provenance and licence of `data/other.csv` and `data/other2.csv` still need to be documented before either file is used or counted.
- **Labels:** `positive`, `negative`, `neutral`. Use `templates/ANNOTATION_GUIDE.md`; neutral is for factual statements without clear expressed polarity, including mildly favorable facts without explicit approval.
- **Splits:** Target 60/20/20 train/dev/test per label, with related examples grouped into one split and all test items independently reviewed. All 116 rows marked `llm_generated` are currently in train. After five native-speaker label corrections, the present counts are:

  | Label | Train | Test | Dev | Total |
  |---|---:|---:|---:|---:|
  | Negative | 69 | 23 | 23 | 115 |
  | Positive | 69 | 23 | 20 | 112 |
  | Neutral | 69 | 23 | 26 | 118 |

  Rebalance only after annotations are settled; do not change a human-adjudicated label just to make counts equal.
- **People and roles recorded in the plan:** Data: Abelle Emmanuel (`contributor_001`) and Innocent Mukiza (`contributor_002`). Review: Innocent Mukiza (`reviewer_001`). Code and documentation: Abelle Emmanuel. The README lists Atta Wasike and Amana Achieng Okello as members, but this repository does not record their specific work; ask them to provide it.
- **Model:** `train.py` uses character TF-IDF (2–5 grams) with a linear SVM and a majority-class baseline. The existing dev metrics predate the latest label corrections and must be recomputed before reporting them.
- **Risks / help needed:** Team availability is a schedule risk. Row-level native-speaker review evidence is incomplete in the repository; reconcile review metadata before submission. Verify the provenance/licence of the separate raw data files.
- **Organizer clarification (10 November 2026):** AfriSenti Kinyarwanda is allowed for sentiment analysis; create new records if the available dataset is inadequate; synthetic examples may be used only for training when data is inadequate and must not be used for testing or evaluation. The reply does not settle external-data counting toward 300 or whether human review makes synthetic data acceptable for evaluation.
