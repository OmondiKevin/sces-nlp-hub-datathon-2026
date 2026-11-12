# Data plan: Team 10

- **Track:** B, sentiment (positive / negative / neutral), sentence level.
- **Language:** Kikuyu (`ki`).  **Domain:** campus cafeteria.
- **Target size:** at least 300 records, at least 100 per label. **Achieved:** 325 after 5 rows were dropped by the reviewer (110 positive, 107 negative, 108 neutral).
- **Sources:** no Kikuyu sentiment corpus was available. English source sentences were written by an AI (Claude), then translated and adapted into Kikuyu by one team member (`source_method = human_localised`). No scraped or Common Voice data. No personal data.
- **Splits:** random with seed 10; per label 20 test, 20 dev, the rest (67-70) train. Test rows are drawn only from independently reviewed rows. `assign_splits.py` keeps rows with the same `group_id` together; each row has its own group_id (its English source ID), so we did not separately check for near-paraphrases across splits.
- **Review plan:** a second fluent speaker checks every test row. Done for all 60 test rows by a Kikuyu-speaking family member of a team member (the two teammates were unreachable). See QUALITY_NOTE.md.
- **Exclusions:** 5 rows dropped by the reviewer, listed in `data/exclusion_log.csv`.
- **Model:** character n-gram TF-IDF + logistic regression, against a majority-class baseline.
