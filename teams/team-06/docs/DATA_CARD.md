# Dataset Card — Team 6 Luganda Intent Corpus v1

## 1. Dataset Overview

The **Team 6 Luganda Intent Corpus** is a collection of 250 human-authored Luganda utterances developed for an intent classification research prototype under Track A.

The dataset is designed to support the classification of written Luganda requests into ten predefined MASSIVE-aligned intent categories. It was created by Team 6 — Data Buddies and independently reviewed by an external fluent Luganda speaker.

| Field | Description |
|---|---|
| Dataset Title | Team 6 Luganda Intent Corpus |
| Dataset Version | `v1` |
| Language | Luganda (`Luganda` in the `language` column) |
| Task | Intent Classification |
| Number of Intent Labels | 10 MASSIVE-aligned categories |
| Intended Use | Request routing in a prototype assistant, teaching and evaluation |
| Out-of-Scope Use | Real-world action execution, production deployment and unsupported claims about Luganda varieties |
| Total Records | 250 accepted records |
| Records per Intent | 25 |
| Dataset Splits | 150 training / 50 development / 50 testing |
| Split Distribution per Intent | 15 training / 5 development / 5 testing |

## 2. Intended Use

### 2.1 Primary Intended Uses

The dataset is intended for:

- Training and evaluating a machine learning model for Luganda intent classification.
- Demonstrating request routing in a prototype conversational assistant.
- Educational purposes and research into natural language processing for Luganda.
- Exploring the application of intent classification to a language with limited available digital language resources.
- Analysing the performance and limitations of a small, human-authored intent classification dataset.

### 2.2 Out-of-Scope Uses

The dataset is not intended for:

- Executing real-world user requests or performing actual assistant actions.
- Production deployment in commercial or public-facing conversational systems.
- Making claims that the dataset represents all Luganda speakers, dialects or regional varieties.
- Treating the model's predictions as guaranteed interpretations of user intentions.
- Making broad claims about the accuracy of Luganda natural language understanding based on this small dataset.

## 3. Dataset Composition

The corpus contains 250 accepted utterances distributed equally across ten intent categories.

| Dataset Split | Records | Percentage |
|---|---:|---:|
| Training | 150 | 60% |
| Development | 50 | 20% |
| Testing | 50 | 20% |
| **Total** | **250** | **100%** |

Each intent category contains 25 records, distributed as follows:

- 15 training records.
- 5 development records.
- 5 testing records.

### 3.1 Intent Categories

The ten intent categories are:

1. `weather_query`
2. `datetime_query`
3. `alarm_set`
4. `calendar_set`
5. `calendar_query`
6. `lists_createoradd`
7. `lists_query`
8. `play_music`
9. `news_query`
10. `qa_definition`

The labels follow the MASSIVE intent schema. The contributed utterances themselves are original human-authored Luganda text.

## 4. Dataset Fields and Structure

The contribution file is provided as:

`data/contribution.csv`

It contains the following 15 columns:

| Field | Description |
|---|---|
| `record_id` | Unique identifier assigned to each utterance. |
| `language` | Language of the utterance, recorded as `Luganda`. |
| `text` | Original Luganda request text. |
| `label` | Assigned intent category. |
| `source_dataset` | Dataset source identifier, recorded as `team_authored`. |
| `source_version` | Source version, recorded as `v1`. |
| `source_record_id` | Identifier associated with the original source record. |
| `source_url` | Source URL; recorded as `not_applicable` for original team-authored data. |
| `source_method` | Method of data creation, recorded as `original_human`. |
| `licence_or_permission` | Permission basis, recorded as `documented_contributor_permission`. |
| `contributor_code` | Pseudonymous identifier for the data contributor. |
| `reviewer_code` | Pseudonymous identifier for the independent reviewer. |
| `review_status` | Status of the independent review. |
| `group_id` | Identifier used to keep related utterance variants within the same dataset split. |
| `split` | Assigned dataset partition: `train`, `dev` or `test`. |

## 5. Data Sources and Provenance

The corpus consists of original human-authored Luganda utterances. The MASSIVE dataset was used as a reference for the intent label schema, not as a source of contributed records.

| Provenance Field | Value |
|---|---|
| Source Method | `original_human` |
| Source Dataset | `team_authored` |
| Source Version | `v1` |
| Source URL | `not_applicable` |
| Licence / Permission | `documented_contributor_permission` |
| Contributor Code | `T06-A` |
| Reviewer Code | `REV-LG-2026` |
| Review Status | All 250 records marked `independently_reviewed` |

### 5.1 Contributor and Reviewer Information

- **Contributor (`T06-A`):** Poni Yokwe, responsible for authoring the Luganda utterances.
- **Reviewer (`REV-LG-2026`):** An external fluent Luganda speaker who was not an author of the reviewed records.

All 250 records underwent independent review. This includes all 50 records in the testing split.

### 5.2 Permission Documentation

Written contributor consent is retained privately and is not included in the public GitHub repository for privacy reasons.

The permission basis and supporting provenance information are documented in `SOURCE_LOG.md`.

## 6. Privacy and Personal Data

The contributed request texts were reviewed for personal and sensitive information.

The following information does not appear in the request texts:

- Personal names.
- Phone numbers.
- Admission numbers.
- Speaker identification numbers.
- Demographic information.
- Other personal identifying details.

Contributor and reviewer identities are represented in the dataset using pseudonymous codes rather than personal names.

The private permission evidence is kept separately from the public dataset documentation.

## 7. Data Cleaning and Known Issues

### 7.1 Duplicate Record Identifiers

During the initial dataset validation, the validator identified 50 duplicated `record_id` values.

The issue originated in the original review log, where the same identifier namespace was reused across paired intent categories:

- `LG-LIS-*` was reused for `lists_createoradd` and `lists_query`.
- `LG-CAL-*` was reused for `calendar_set` and `calendar_query`.

The validator correctly rejected these duplicate identifiers.

### 7.2 Resolution

The duplicate identifiers were corrected using `fix_ids.py`.

The second occurrence of each duplicated identifier was assigned the suffix `_2`.

For example:

- Original identifier: `LG-LIS-024`
- Corrected second identifier: `LG-LIS-024_2`

The same correction approach was applied to all 50 duplicated identifiers.

The original review log was preserved unchanged as:

`evidence/REVIEW_LOG.csv`

**Impact on dataset content:** The correction affected record identifiers only. The original Luganda text and assigned intent labels were not changed.

## 8. Known Limitations

The dataset has several limitations that should be considered when using or interpreting it.

### 8.1 Small Dataset Size

The corpus contains 250 records, with only five testing examples per intent category.

Consequently, evaluation results may be sensitive to individual predictions and have considerable statistical uncertainty.

### 8.2 Limited Language Variety Coverage

The dataset represents one authored collection of Luganda utterances rather than a broad sample of regional and linguistic varieties.

It should not be assumed to represent all Luganda speakers or dialects.

### 8.3 Limited Contributor Diversity

The original utterances were authored by one contributor. Independent review provides an additional quality check, but does not replace broad participation from different Luganda-speaking communities.

### 8.4 Surface-Level Model Representation

The starter baseline uses character-level TF-IDF (n-grams of length 2–5) as the text representation, paired with a Logistic Regression classifier.

This approach captures surface patterns in written text but may fail to understand certain linguistic features, including negation, complex sentence structures and changes in meaning.

The model's test-set errors and related observations are documented in `QUALITY.md`.

### 8.5 Unsupported Input Handling

The prototype application assigns a known intent category even when an input may fall outside the supported categories.

This limitation is demonstrated in the application and should be considered when interpreting its predictions.

### 8.6 Limited Generalisation

The dataset and evaluation results do not establish reliable performance on unseen Luganda varieties, broader speaker populations or real-world conversational requests.

## 9. Quality Assurance and Evaluation

Dataset quality assurance involved automated structural validation and independent human review.

The automated validator checks dataset structure, split sizes and record ID uniqueness.

Human review covers:

- Naturalness of Luganda expressions.
- Suitability of the assigned intent labels.
- Preservation of the intended meaning from the English prompts.
- Data provenance and permission documentation.

The final structural validation result was:

**`PASS: 250 records`**

Detailed quality findings and model evaluation observations are documented in `QUALITY.md`.

Additional annotation decisions are available in `ANNOTATION_GUIDE.md`.

## 10. Maintenance and Versioning

| Field | Value |
|---|---|
| Current Version | `v1` |
| Maintainers | Team 6 — Data Buddies |
| Project Repository | See `README.md` |
| Planned Updates | No further updates planned after submission. |

The dataset is maintained as a research and educational contribution for the current project submission.

Any future modifications would require appropriate version updates and corresponding documentation of changes.

## 11. Related Documentation

The following documents provide additional information about the corpus and its development:

- `README.md` — Project overview, setup instructions and model evaluation.
- `DATA_PLAN.md` — Dataset development and collection process.
- `ANNOTATION_GUIDE.md` — Intent definitions, annotation rules and review protocol.
- `SOURCE_LOG.md` — Data provenance and permission records.
- `QUALITY.md` — Dataset quality assurance and evaluation findings.
- `CONTRIBUTIONS.md` — Team member responsibilities and contributions.
- `SUBMISSION_MANIFEST.md` — Final submission contents.

---

**Team 6 — Data Buddies**  
*Team 6 Luganda Intent Corpus v1 | Track A — Intent Classification*