# Contributions and AI-Use Statement — Team 6: Data Buddies

## 1. Team contributions

| Member | Contributor code | Contribution | Evidence |
|---|---|---|---|
| Poni Yokwe | `T06-A` | Authored 250 Luganda utterances based on the provided English meaning prompts, using natural Luganda phrasing and applying the agreed intent-label boundaries. | `data/contribution.csv`, `evidence/REVIEW_LOG.csv` |
| Sydney Aisha | `T06-B` | Set up the repository, trained the character TF-IDF and Logistic Regression baseline, prepared the model artifacts, and built and ran the  custom web demonstration application. | `artifacts/intent/`, mobile_app.py, mobile/index.html |
| Tiffany Wanjiru | `T06-C` | Prepared the data plan, annotation guide, dataset card, source log, quality report, and submission manifest. Ran the dataset validator, resolved record ID collisions, and assembled the submission package. | `DATA_PLAN.md`, `ANNOTATION_GUIDE.md`, `DATA_CARD.md`, `SOURCE_LOG.md`, `QUALITY.md`, `SUBMISSION_MANIFEST.md`, `build_contribution.py`, `fix_ids.py` |

## 2. Independent reviewer contribution

`REV-LG-2026` independently reviewed all 250 Luganda utterances for naturalness and intent-label fit.

All 50 test records, representing five examples per intent, were independently reviewed before final model evaluation.

The reviewer is an external fluent Luganda speaker who did not author the records being reviewed. Per-record review decisions are documented in `evidence/REVIEW_LOG.csv`.

## 3. AI-use disclosure

ChatGPT (OpenAI) was used to assist with drafting, structuring, and refining the project's Markdown documentation. This included the README, data plan, annotation guide, dataset card, source log, quality report, contributions statement, and submission manifest.

The team remains responsible for reviewing the final documentation and ensuring that its contents accurately reflect the dataset, implementation, evidence, and project decisions.

AI tools were not used to generate the 250 Luganda utterances included in `data/contribution.csv`. The utterances were authored by a team member and independently reviewed by `REV-LG-2026`.

No bulk automatic translation or AI-authored sentences were included as human-authored dataset contributions. The intent labels were assigned using the project's annotation guide and the MASSIVE-aligned label schema.

AI tools also assisted with drafting the Python data-preparation scripts build_contribution.py and fix_ids.py. Their output was inspected line by line, and validate.py was run to confirm the resulting file passes structural validation (PASS: 250 records).

AI assistance with documentation did not replace the team's responsibility for checking the accuracy of the project information or the reviewer's responsibility for checking the Luganda utterances.

## 4. Contributions not claimed by the team

The following are not counted as original Team 6 dataset contributions:

- **Starter kit practice rows:** These were supplied for practice and count as zero original contribution.
- **MASSIVE dataset records:** No MASSIVE utterances are included in `data/contribution.csv`. Only the MASSIVE-aligned intent-label schema was used.
- **Common Voice records:** No Common Voice utterances are included in the contribution file.
- **Starter kit code:** The original starter code is acknowledged as an upstream resource. The team's work and adaptations are documented separately, with credit provided in `SOURCE_LOG.md`.

## 5. Contribution and evidence integrity

The contribution claims in this document are based on the team's stated responsibilities and the project evidence identified above.

All contributions are attributed to the members responsible for the corresponding work. The team acknowledges the starter kit and external label schema used in the project and does not claim these resources as original work.