# Data Plan — Team 6

## 1. Project Information

| Field | Description |
|---|---|
| Team | 6 — Data Buddies |
| Track | A — Intent Classification |
| Primary Language | Luganda (`Luganda` in the dataset) |
| Intent Labels | 10 MASSIVE-aligned intent categories (see `ANNOTATION_GUIDE.md`) |
| Source Method | `original_human` — original utterances authored in Luganda by Poni Yokwe |
| Source Dataset | `team_authored` |
| Source Version | `v1` |
| Source URL | `not_applicable` |
| Licence / Permission | `documented_contributor_permission` (evidence retained privately; see `SOURCE_LOG.md`) |
| Contributor Code | `T06-A` — Poni Yokwe |
| Reviewer Code | `REV-LG-2026` — External fluent Luganda reviewer, independent of the authorship process |
| Target Dataset Size | 250 accepted records (25 per intent) |
| Dataset Split | 15 training, 5 development and 5 testing records per intent |

**Optional Stretch Goal:** Not attempted. The team's effort was prioritised towards independent language review, dataset quality and error analysis.

## 2. Data Collection and Preparation Process

The following process was used to develop and prepare the contributed dataset.

1. **Task and Language Selection:** Track A (Intent Classification) and Luganda were selected before annotation began. The team maintained the selected task and language throughout the data preparation process.

2. **Utterance Authorship:** A total of 250 Luganda utterances were authored by Poni Yokwe using the provided English meaning prompts as guidance. The utterances were written to reflect natural Luganda expressions rather than being direct, word-for-word translations.

3. **Dataset Split Planning:** A stratified dataset split was established before model training. Each of the ten intent categories was assigned 15 training records, 5 development records and 5 testing records.

4. **Independent Language Review:** All 250 utterances were submitted to the external reviewer, `REV-LG-2026`, for independent assessment of linguistic naturalness and intent-label suitability. Every record was marked `independently_reviewed`, including all 50 records assigned to the test set.

5. **Contribution File Generation:** The review log was processed using `python build_contribution.py` to generate `data/contribution.csv`, following the 15 required starter-kit columns.

6. **Record ID Correction:** During the initial validation, the automated validator identified 50 duplicate `record_id` values. The duplicates resulted from numbering being restarted within paired intent categories. For example, the `LG-LIS` prefix had been reused across `lists_createoradd` and `lists_query`. The issue was corrected using `fix_ids.py`, which appended `_2` to the second occurrence of each duplicated ID. The original `REVIEW_LOG.csv` was preserved unchanged as provenance evidence.

7. **Final Validation:** The contribution dataset was validated successfully, returning `PASS: 250 records`. This confirmed structural compliance. Linguistic quality, intent-label suitability and data permissions were assessed separately through human review and documented in `QUALITY.md` and `SOURCE_LOG.md`.

## 3. Dataset Split Strategy

The dataset was divided using a stratified approach to maintain equal representation across all ten intent categories.

| Split | Records per Intent | Number of Intents | Total Records |
|---|---:|---:|---:|
| Training | 15 | 10 | 150 |
| Development | 5 | 10 | 50 |
| Testing | 5 | 10 | 50 |
| **Total** | **25** | **10** | **250** |

### 3.1 Leakage Prevention

Each record was assigned its own unique group_id. The final dataset contains no duplicate or closely related utterance variants (0 duplicate texts verified), so no cross-split grouping was necessary.

### 3.2 Test Set Isolation

The 50 testing records were held back from model training and development-stage tuning.

Model selection and related development decisions were based on the development dataset. The test dataset was reserved for final evaluation of the trained model.

## 4. Data Sources and Originality

The dataset was developed with the following source and originality considerations:

- **Original Human Authorship:** All 250 contributed utterances were authored in Luganda by the designated team contributor, Poni Yokwe.
- **Independent Review:** The contributed records were independently reviewed by a fluent Luganda reviewer who was not the author of the reviewed records.
- **MASSIVE Reference:** The MASSIVE dataset was used as a reference for its intent label schema. No original MASSIVE dataset records were included in `data/contribution.csv`.
- **No Borrowed Common Voice Text:** Common Voice text was not used as a source of contributed utterances.
- **No Bulk AI-Generated Data:** Bulk AI-generated utterances were not used to meet the dataset contribution target.
- **No Unchanged Downloaded Records:** Downloaded records were not counted towards the 250 original contribution target.

## 5. Validation and Quality Assurance

Dataset validation involved both automated and human review processes.

| Validation Area | Method | Result / Evidence |
|---|---|---|
| Dataset structure | Starter-kit validator | `PASS: 250 records` |
| Language naturalness | Independent fluent Luganda review | Documented in `QUALITY.md` |
| Intent-label suitability | Independent reviewer assessment | Documented in `QUALITY.md` |
| Data permissions | Contributor permission documentation | Evidence referenced in `SOURCE_LOG.md` |
| Record ID uniqueness | Automated validation and ID correction | Duplicate IDs corrected using `fix_ids.py` |
| Split distribution | Stratified allocation | 150 training, 50 development and 50 testing records |
| Data leakage prevention | Group-based split assignment | Related variants retained within the same split |

The automated validator was used to verify structural requirements. It was not treated as proof of linguistic accuracy or annotation quality.

## 6. Project Constraints and Scope

The following constraints defined the scope of the data contribution:

1. The dataset was limited to 250 accepted Luganda utterances.
2. Each of the ten intent categories contained exactly 25 records.
3. All contributed records underwent independent language and label review.
4. The original authorship and permission information was retained for documentation and provenance.
5. The MASSIVE dataset was used only as a reference for intent categories, not as a source of contributed records.
6. No optional stretch dataset contribution was attempted.

## 7. Supporting Documentation

The following documents provide additional information about the dataset development process:

| Document | Purpose |
|---|---|
| `ANNOTATION_GUIDE.md` | Defines the annotation rules and intent-label guidelines. |
| `DATA_CARD.md` | Describes the dataset, its composition and intended use. |
| `SOURCE_LOG.md` | Documents data provenance, source information and permissions. |
| `QUALITY.md` | Records dataset quality checks and independent review findings. |
| `CONTRIBUTIONS.md` | Documents individual team contributions. |
| `SUBMISSION_MANIFEST.md` | Lists and describes the final submission contents. |

---

**Team 6 — Data Buddies**  
*Luganda Intent Classification | Track A*