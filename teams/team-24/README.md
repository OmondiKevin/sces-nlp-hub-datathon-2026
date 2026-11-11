# Team 24 | Kiswahili 5: intent classification

## Team and task

- **Team:** 24, Kiswahili 5
- **Members:** Moses Kibet ([Moses374](https://github.com/Moses374)), Krysia Njoroge, and Nathan Njuguna. Krysia's and Nathan's GitHub usernames were not provided.
- **Track:** A — intent classification
- **Language and variety:** Kiswahili (`sw-KE`), everyday Kenyan Swahili in a spoken-request register
- **Original team repository:** [Moses374/Team24-Kiswahili](https://github.com/Moses374/Team24-Kiswahili)
- **Source commit used:** [`9d4eeda6c5e85a9219c17a57f29d8865d0a95e23`](https://github.com/Moses374/Team24-Kiswahili/commit/9d4eeda6c5e85a9219c17a57f29d8865d0a95e23) (`v1.0-submission`)

## Idea and approach

We built a small Kiswahili intent classifier for requests to a simulated assistant. It predicts one of ten actions, including asking about weather, setting a calendar event, reading a list, or playing music. We chose everyday Kenyan Swahili because the project focuses on a language variety underrepresented in common assistant examples.

The team wrote and reviewed the contribution data, applied the organiser starter kit's label definitions, and trained its character n-gram TF-IDF/logistic-regression baseline. The Streamlit demo uses the trained model and displays the prediction and confidence. The project reuses the organiser's starter kit code and libraries; details and AI assistance are recorded in `docs/CONTRIBUTIONS.md`.

## Data and review

The contribution contains **262 team-authored examples**: 159 train, 51 development, and 52 test. It covers ten labels, with at least 15 train, 5 development, and 5 test examples for each. All rows are recorded as Kiswahili text authored by team members; 110 collected external rows were excluded due to missing licence and provenance. The CSV includes the split and review fields.

Krysia Njoroge authored 196 examples; Nathan Njuguna authored 66. Moses Kibet reviewed 43 test examples and the train/development examples; Nathan reviewed the other 9 test examples. Every test row was reviewed by someone other than its recorded author. The validator passes, though it cannot assess fluency or data rights. See [data card and source log](docs/DATA_CARD.md), [annotation guide](docs/ANNOTATION_GUIDE.md), [quality report](docs/QUALITY.md), [data plan](docs/DATA_PLAN.md), and [contributions and AI use](docs/CONTRIBUTIONS.md).

## Code and how to run

Python 3.10 or later is recommended. From this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate.py --track intent --data data/contribution.csv
python train.py --track intent --data data/contribution.csv
python evaluate.py --track intent --data data/contribution.csv
python -m streamlit run app.py
```

The model is rebuilt by the training command and saved under `artifacts/intent/`. Evaluation outputs include metrics, per-label results, and test predictions in that folder. The contribution CSV includes train/dev/test splits. Dependency constraints are in `requirements.txt`.

## Results and limitations

On the frozen test split (52 examples), the baseline reached **0.808 accuracy** and **0.790 macro-F1**; development accuracy was 0.824 and development macro-F1 was 0.816. The majority-class comparator's macro-F1 was 0.021. See [test metrics](artifacts/intent/test_metrics.json), [development metrics](artifacts/intent/dev_metrics.json), [per-label report](artifacts/intent/per_label_report.csv), and [test predictions](artifacts/intent/test_predictions.csv).

The weakest test label was `calendar_query` (F1 0.333), followed by `lists_query` (0.600). The small test set has only five or six examples per label, so scores can change substantially with a few examples. Other limitations include one Kiswahili variety, a small number of authors, AI-suggested wording in 35 examples, and the model's tendency to learn topic words instead of distinguishing a question from a command. The quality report describes five representative observed errors and discloses repeated test-set evaluation. A later cross-validation experiment on train/development data is marked as post-hoc; its improved setting was not evaluated on the test set.

## Presentation and demo video

- [Team 24 presentation and demo](https://youtu.be/TZWTq4xrssQ)

## Required materials

- Contribution data and splits: `data/contribution.csv`
- Annotation guide: `docs/ANNOTATION_GUIDE.md`
- Source log and terms: `docs/DATA_CARD.md`
- Dataset card: `docs/DATA_CARD.md`
- Quality and review report: `docs/QUALITY.md`
- Contribution and AI-use statement: `docs/CONTRIBUTIONS.md`
- Evaluation files: `artifacts/intent/`
- Runnable code and dependencies: repository root and `requirements.txt`
- Trained artefact: reproduce with the training command above; generated model files are not committed
- Video: [YouTube demo](https://youtu.be/TZWTq4xrssQ)

## Attribution and permissions

The team reuses code and templates from the Strathmore NLP Hub Datathon starter kit v2.0; see `LICENSE_CODE.txt` and `docs/CONTRIBUTIONS.md`. No rows from MASSIVE, AfriSenti, Common Voice, or the excluded Rogendo dataset are included in the contribution. The team's data release terms are still pending the organisers' terms; permission evidence is held separately and is not included in this public submission.
