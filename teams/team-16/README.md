# Team 16 | Kinyarwanda Sentiment Analysis

## Team and task

- Team number and name: Team 16 — Strathmore NLP Datathon Team 16 (Kinyarwanda)
- Three members and their contributions (names/GitHub usernames only): Atta Wasike; Abelle Emmanuel; Amana Achieng Okello
- Working language/variety: Kinyarwanda
- Track: B sentiment
- Original team repository URL: https://github.com/Wazzicus/nlp-datathon-2026-team-16-kinyarwanda/
- Full source commit SHA for the version submitted: e4fbca02f13ca4200a04cc0c187ce41d63d1bd1e

## Idea and approach

SENTI-RW addresses sentiment classification for Kinyarwanda, a low-resource language with limited NLP tooling. The goal is to help users classify short Kinyarwanda texts into positive, negative or neutral sentiment categories in a way that is lightweight and usable for research and demos.

The dataset was reviewed and split into train/dev/test subsets, then used to train a character-level TF-IDF model with a LinearSVC classifier. A reusable Python predictor and a Streamlit app were built on top of the best-performing configuration, with the final baseline selected based on development-set performance and then evaluated on the held-out test set. This project reuses established scikit-learn tooling and combines it with a small, task-specific Kinyarwanda pipeline.

## Data and review

The original contribution dataset contains 345 labelled records across three sentiment classes, with the following split:

- Training: 207 examples
- Development: 69 examples
- Test: 69 examples
- Total: 345 examples

The training data includes 69 examples per class. Additional sources such as AfriSenti and KINNEWS/KIRNEWS were reviewed during experimentation, but the original contribution dataset produced the strongest development-set performance and was therefore used for the final baseline. The final model was trained on the original contribution dataset only.

Dataset provenance and annotation details are retained in the project data schema and documentation. Source licensing and redistribution terms must be checked before public data redistribution; the current draft does not claim unrestricted redistribution beyond the project’s permitted workflow. Review quality checks were based on train/dev/test separation, per-class metric inspection and error analysis on held-out predictions.

## Code and how to run

Relevant project files include:

- app.py — Streamlit demo interface
- predictor.py — reusable prediction module
- test_predictor.py — inference and regression checks
- core.py — shared project utilities
- validate.py — dataset validation utilities
- requirements.txt — Python dependencies
- README.md — project overview
- data/ — dataset files
- artifacts/ — trained model and experiment outputs
- docs/ — supporting documentation

Environment and dependency requirements:

- Python 3.10 or later
- pip
- Git
- scikit-learn, pandas, joblib and Streamlit

Installation:

```bash
git clone <repository-url>
cd <repository-directory>
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate
pip install -r requirements.txt
```

Validation and demo commands:

```bash
# Run the demo app
streamlit run app.py
```

The app is normally served at:

```text
http://localhost:8501
```

Python inference example:

```python
from predictor import SentimentPredictor

predictor = SentimentPredictor()
result = predictor.predict("Nishimiye cyane uko iki gikorwa cyagenze.")

print(result["sentiment"])
print(result["decision_scores"])
```

The model output includes the predicted sentiment and the raw LinearSVC decision scores; these are not calibrated probabilities and should not be interpreted as percentage confidence values.

## Results and limitations

The final baseline was evaluated on the held-out test set with the following results:

| Metric | Result |
|---|---:|
| Accuracy | 65.22% |
| Macro-F1 | 65.28% |

Per-class F1 scores:

| Sentiment | F1-score |
|---|---:|
| Positive | 59.6% |
| Negative | 66.7% |
| Neutral | 69.6% |

The majority-class baseline macro-F1 was 16.7%, and the development macro-F1 was approximately 76.67%, compared with 65.28% on the test set. This gap indicates that the model generalises less well than it does on the development examples, which is common in small low-resource datasets.

Observed error patterns include:

- Negation and its effect on the overall sentiment of a sentence
- Distinguishing genuine opinion from sentiment-bearing vocabulary used in a factual statement
- Context-dependent sentiment that is not recoverable from local word patterns alone
- Class confusion between neutral and strongly opinionated statements

Limitations include the small training set size, limited generalisation to unseen examples, the lack of deep semantic or contextual understanding, and the subjectivity inherent in human annotation. This means the system is best treated as an experimental research prototype rather than a production-ready sentiment service.

## Presentation and demo video

- Presentation/demo video URL (REQUIRED): TBD before final submission
- Optional second presentation/demo video: TBD
- Optional hosted app URL: TBD


## Required materials

Link each item using a relative path or an accessible external URL:

- Contribution dataset and splits: data\contribution.csv
- Annotation guide: docs\ANNOTATION_GUIDE.md
- Source log and source terms: TBD
- Dataset card: DATA_CARD.md
- Quality/review report: docs\QUALITY.md
- Contribution and AI-use statement: docs\CONTRIBUTIONS.md
- Evaluation outputs and baseline comparison: TBD
- Runnable code and dependency file: requirements.txt and project source files in this repository
- Trained artefacts or reproduction instructions: TBD
- Video link: TBD

## Attribution and permissions

This project builds on established low-resource African-language NLP work, including AfriSenti and KINNEWS/KIRNEWS, and acknowledges the authors and contributors who made those resources available. The work uses standard open-source tooling, especially Python and scikit-learn, as well as the project’s starter-kit structure for the datathon submission workflow.
