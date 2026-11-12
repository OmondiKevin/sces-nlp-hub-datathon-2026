# Team 11 | LuoSense

LuoSense is an experimental Dholuo sentiment-classification project developed for the Strathmore NLP Hub Datathon 2026.

## 1. Team and task

- **Team:** Team 11
- **Project:** LuoSense
- **Working language:** Dholuo
- **Track:** Track B - Sentiment
- **Team members:**
  - **Emma Awuor Ogwayo (@Emzogwayo):** Technical lead. Led technical development and integration, sentiment-classification pipeline, model training and evaluation, Streamlit application, technical troubleshooting, repository integration and submission documentation.
  - **Celestine Mboya:** Identified and sourced the original sentiment dataset; contributed to Dholuo translation, language checking and dataset preparation.
  - **Nicholas Njue:** Prepared and organised the Excel dataset workbook; contributed to data entry, structuring and preparation of the final contribution dataset.
- **Original team repository:** https://github.com/Nexnju/nlp-datathon-2026-team-11
- **Source commit:** `9f39174c8ec9eb7bf9d388b9cff9d2f2abff07a`

## 2. Idea and approach

LuoSense explores three-class sentiment classification for Dholuo text. It uses character-level text features and a Logistic Regression classifier to predict whether a text expresses positive, negative or neutral sentiment.

The project workflow was:

1. Identify an existing Sindhi sentiment dataset and prepare Dholuo draft text.
2. Organise the contribution records, sentiment labels, review metadata and dataset splits.
3. Run structural validation and train a character-level TF-IDF and Logistic Regression model.
4. Evaluate the trained model using development and held-out test data.
5. Develop a Streamlit interface to demonstrate sentiment predictions.

The project uses the datathon starter-kit workflow with a project-specific dataset, trained model and demonstration interface.

## 3. Data and review

the final contribution dataset contains 300 records, balanced across three sentiment classes.

| Sentiment | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| **Total** | **300** |

The dataset is split into:
- Training: 180 records
- Development: 60 records
- Test: 60 records

The dataset metadata records:
- 276 records as `machine_translated`, where translated output was used largely as produced.
- 24 records as `human_localised`, where initial translated drafts were subsequently human-localised.
- 217 self-reviewed records and 83 independently reviewed records.
- All 60 test records have independent-review metadata.

Google Translate was used to produce the initial Dholuo drafts for all 300 records from Sindhi source material. These figures do not establish that all records were manually translated or fully validated by fluent Dholuo speakers.

The structural validator reported:

`PASS: 300 records; language quality, permission and semantic duplicate review remain human responsibilities.`

This confirms structural checks only. It does not certify Dholuo linguistic quality, semantic correctness or redistribution permissions.

### Source dataset and access

The identified source is Ali Nawaz, *Sindhi Sentiment Analysis Dataset*, listed on Mozilla Data Collective:

https://mozilladatacollective.com/datasets/cmrlqkecf00jynu07k7fb90iv

The source listing identifies the licence as CC BY-NC 4.0. The exact downloaded source version and source record IDs were not retained or confirmed. Redistribution permissions for the derivative Dholuo dataset have not been established.

The contribution CSV is therefore not included in this public repository. The dataset should be provided to judges only through an organiser-approved access route.

Further documentation:
- [Annotation guide](docs/annotation_guide.md)
- [Contributions and AI-use statement](docs/contributions.md)
- [Dataset card](docs/dataset_card.md)
- [Data quality report](docs/data_quality_report.md)
- [Evaluation report](docs/evaluation_report.md)
- [Provenance and rights](docs/provenance_and_rights.md)
- [Validator output](submission/evidence/validator_output.txt)

## 4. Code and how to run

### Requirements

The project uses Python and the dependencies listed in `requirements.txt`:

- scikit-learn 1.7.2
- pandas 2.2 or later, below version 3
- Streamlit 1.40 or later, below version 2
- joblib 1.4 or later, below version 2

Create and activate a virtual environment in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Validation, training and evaluation

These commands require the contribution dataset to be available as `data/contribution.csv` through an organiser-approved access route:

```powershell
python validate.py --data data/contribution.csv --track sentiment
python train.py --data data/contribution.csv --track sentiment
python evaluate.py --data data/contribution.csv --track sentiment
```

Training saves the model and development metrics under `artifacts/sentiment/`. Evaluation saves the test metrics and per-label report in the same directory.

### Run the Streamlit demonstration

With the trained model available at `artifacts/sentiment/model.joblib`, run:

```powershell
streamlit run app.py
```

The application loads the sentiment model from `artifacts/sentiment/model.joblib`. Dataset-backed examples require the contribution CSV, which is not included in this public repository pending rights clarification.

## 5. Model results and limitations

The selected classifier is a scikit-learn pipeline consisting of:

- Character-level TF-IDF vectorisation using character n-grams of length 2â€“5.
- Logistic Regression with `max_iter=1000` and `random_state=42`.

### Held-out test results

| Metric | LuoSense model | Majority baseline |
|---|---:|---:|
| Accuracy | 61.67% | 33.33% |
| Macro-F1 | 0.6114 | 0.1667 |

### Per-class test F1

| Class | F1-score |
|---|---:|
| Positive | 0.6512 |
| Negative | 0.5000 |
| Neutral | 0.6829 |

The test set contains 60 records. The confusion matrix below uses the label order positive, negative, neutral.

```text
                 Predicted
Actual          Positive  Negative  Neutral
Positive            14         4        2
Negative             6         9        5
Neutral              3         3       14
```

Development results:
- Accuracy: 70.00%
- Macro-F1: 0.6984

Saved evaluation artefacts:
- [Development metrics](artifacts/sentiment/dev_metrics.json)
- [Test metrics](artifacts/sentiment/test_metrics.json)
- [Per-label report](artifacts/sentiment/per_label_report.csv)
- [Trained model](artifacts/sentiment/model.joblib)

### Limitations

- The dataset is small and derived from Sindhi sentiment material through machine translation and subsequent human localisation of a subset.
- Broader review by proficient Dholuo speakers is needed to assess linguistic naturalness and label validity.
- Structural validation does not establish linguistic quality or semantic correctness.
- The exact source dataset version and original record-level identifiers were not retained.
- Redistribution permissions for the derivative dataset remain unresolved.
- The held-out test set contains only 60 records. The results are preliminary and should not be generalised to all Dholuo text or domains.
- LuoSense is an experimental demonstration, not a production-ready language model.

## 6. Presentation and demo video

**Demo video (YouTube):** ADD YOUTUBE LINK HERE

The demonstration video will show the application, its sentiment-prediction workflow and the project results.

## 7. Required materials

- Contribution dataset: withheld from this public repository pending rights clarification; access should be requested through the datathon organisers.
- Annotation guide: [docs/annotation_guide.md](docs/annotation_guide.md)
- Dataset card: [docs/dataset_card.md](docs/dataset_card.md)
- Data quality report: [docs/data_quality_report.md](docs/data_quality_report.md)
- Contributions and AI-use statement: [docs/contributions.md](docs/contributions.md)
- Provenance and rights: [docs/provenance_and_rights.md](docs/provenance_and_rights.md)
- Evaluation report: [docs/evaluation_report.md](docs/evaluation_report.md)
- Source code: `app.py`, `core.py`, `train.py`, `evaluate.py`, `validate.py`
- Dependencies: [requirements.txt](requirements.txt)
- Trained model and metrics: `artifacts/sentiment/`
- Validator evidence: [submission/evidence/validator_output.txt](submission/evidence/validator_output.txt)

## 8. Attribution and permissions

This project builds on the Strathmore NLP Hub Datathon starter kit and the Sindhi Sentiment Analysis Dataset attributed to Ali Nawaz on Mozilla Data Collective. Google Translate was used to produce the initial Dholuo drafts from Sindhi source material.

The source dataset is listed under CC BY-NC 4.0. The exact source version and record-level identifiers were not retained, and redistribution permissions for the derivative Dholuo dataset remain unresolved. The contribution CSV is therefore withheld from this public repository pending organiser guidance. No unrestricted redistribution claim is made.

The project code is accompanied by `LICENSE_CODE.txt`.

