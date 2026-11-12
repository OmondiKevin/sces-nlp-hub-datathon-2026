# Team Contributions and AI-Use Statement

**Project:** LuoSense  
**Team:** 11  
**Track:** Track B — Sentiment  
**Working language:** Dholuo  
**Submission date:** 12 November 2026

## 1. Project overview

LuoSense is an experimental three-class Dholuo sentiment-classification project developed for the Strathmore NLP Hub Datathon 2026. It classifies text as positive, negative or neutral using character-level TF-IDF features and Logistic Regression.

## 2. Team contributions

| Member | Contributions |
|---|---|
| Emma Awuor Ogwayo (@Emzogwayo) | Technical lead. Led technical development and integration, the sentiment-classification pipeline, model training and evaluation, Streamlit application, troubleshooting, repository integration, technical documentation and official submission. |
| Celestine Mboya | Identified and sourced the original sentiment dataset; contributed to Dholuo translation, language checking and dataset preparation. |
| Nicholas Njue | Prepared and organised the Excel dataset workbook; contributed to data entry, structuring and preparation of the final contribution dataset. |

These descriptions reflect the roles and work reported by the team. They do not imply equal contributions or assign individual record-level counts.

## 3. Dataset preparation and provenance

The contribution dataset contains 300 records, balanced across positive, negative and neutral sentiment, with 100 records per class. The split is 180 training, 60 development and 60 test records.

All 300 initial text drafts were produced using Google Translate from Sindhi source material. The dataset metadata records:
- 276 records as `machine_translated`.
- 24 records as `human_localised`.
- 217 records as self-reviewed.
- 83 records as independently reviewed.
- All 60 test records have independent-review metadata.

These metadata labels describe the recorded workflow. They do not independently establish reviewer fluency, linguistic expertise or complete semantic accuracy.

The source was the Ali Nawaz Sindhi Sentiment Analysis Dataset listed on Mozilla Data Collective under CC BY-NC 4.0. The exact downloaded version and source record IDs were not retained.

## 4. Technical implementation

The technical implementation was led by Emma Awuor Ogwayo.

The classifier uses character-level TF-IDF features with n-gram range 2–5 and Logistic Regression configured with `max_iter=1000` and `random_state=42`.

The work included:
- Building and integrating the text-classification pipeline.
- Training and evaluating the classifier.
- Comparing results against a majority-class baseline.
- Developing the Streamlit demonstration application.
- Saving the trained model and evaluation artefacts.
- Integrating project files and preparing technical documentation.

## 5. Evaluation results

The held-out test set contained 60 records.

| Metric | Model | Majority baseline |
|---|---:|---:|
| Accuracy | 61.67% | 33.33% |
| Macro-F1 | 0.6114 | 0.1667 |

Per-class test F1:
- Positive: 0.6512
- Negative: 0.5000
- Neutral: 0.6829

These results are experimental and should be interpreted in light of the dataset size, machine-translation process and limitations of the available language review.

## 6. Tools and AI use

| Tool or resource | Use |
|---|---|
| Mozilla Data Collective | Source dataset discovery |
| Google Translate | Initial translation drafts for the 300 records |
| Python and pandas | Data handling and preparation |
| scikit-learn | TF-IDF features, Logistic Regression and evaluation |
| joblib | Model artefact persistence |
| Streamlit | Demonstration interface |
| Git and GitHub | Version control and repository collaboration |
| Visual Studio Code and PowerShell | Development and project administration |
| AI assistance tools | Technical troubleshooting, coding support and documentation assistance |

Machine translation and AI-assisted technical work are disclosed here. They should not be interpreted as evidence that the Dholuo text was independently validated by fluent speakers.

## 7. Validation and quality limitations

The dataset validator reported:

`PASS: 300 records; language quality, permission and semantic duplicate review remain human responsibilities.`

This result confirms structural checks performed by the validator. It does not certify linguistic quality, semantic correctness, dataset permissions or the absence of duplicates requiring human judgement.

The validator output is retained at `submission/evidence/validator_output.txt`.

## 8. Data access and redistribution

The source dataset listing identifies a CC BY-NC 4.0 licence. However, the exact source version and record-level provenance were not retained, and permission to redistribute the derivative Dholuo contribution dataset has not been established.

For that reason, `data/contribution.csv` and the source workbook are not included in this public repository. The team can provide the data to the organisers through an approved access route if requested.

## 9. Declaration

This statement records the team's reported contributions, data preparation process, use of machine translation and AI assistance, and known limitations. It does not claim that every record was manually translated or linguistically validated, or that all team members contributed equally.

