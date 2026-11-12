# Team 06 | Luganda Intent Classification

## Team and task

- **Team number and name:** Team 6 — Data Buddies
- **Team Members and their contributions:**
  - **Poni Yokwe** — Created and curated the 250 Luganda utterances.
  - **Sydney Aisha** — Trained and evaluated the model and developed the web demo.
  - **Tiffany Wanjiru** — Prepared the data, resolved ID issues, documented the project and packaged the submission.
- **Working language/variety:** Luganda
- **Track:** A — Intent classification
- **Original team repository URL:** https://github.com/syd-xo/DataBuddies.git
- **Full source commit SHA for the version submitted:** `52b0deb52806f8b681d7dd2aaa99744d7c815b13`

## Idea and approach

The project is a Luganda intent-classification prototype designed to identify what a user wants when they submit a request. It demonstrates how a language-specific system could route requests to appropriate functions, making digital assistants more accessible to Luganda speakers.

The team:
1. Created 250 original Luganda utterances across 10 intent labels, with 25 utterances per label.
2. Organised the data into training, development and test splits, and arranged independent review by a fluent Luganda speaker.
3. Prepared and validated the contribution dataset, including resolving duplicate record IDs without changing the utterances or their labels.
4. Trained a character-level TF-IDF and Logistic Regression classifier.
5. Built a custom web demo to display predicted intents and illustrative responses.

The original contribution is the Luganda dataset, its review and the project-specific implementation. The project reuses the starter kit structure and MASSIVE-aligned intent labels.

## Data and review

- **Accepted contribution records:** 250
- **Intent coverage:** 10 intents, with 25 records per intent.
- **Training split:** 150 records.
- **Development split:** 50 records.
- **Test split:** 50 records.
- **Data source:** Original team-authored Luganda utterances.
- **Source version:** v1.
- **Permission:** `documented_contributor_permission`; written permission evidence is retained privately.
- **Independent review:** All 250 records, including all 50 test records, were reviewed by an independent fluent Luganda speaker identified as `REV-LG-2026`. The reviewer did not author the reviewed records.
- **Quality checks:** 0 duplicate text values were found. Duplicate record IDs were resolved by adding `_2` to the second occurrence. No utterance text or intent labels were changed during this correction.

The structural validation command is:

```bash
python validate.py --track intent --data data/contribution.csv
```

The validator checks structural requirements. It does not independently establish language quality, semantic correctness or permission.

Related materials:

- Contribution dataset and splits: `data/contribution.csv`
- Annotation guide: `docs/ANNOTATION_GUIDE.md`
- Source log and source terms: `docs/SOURCE_LOG.md`
- Dataset card: `docs/DATA_CARD.md`
- Quality and review report: `docs/QUALITY.md`
- Data plan: `docs/DATA_PLAN.md`

## Code and how to run

The project uses Python 3.10 or later, scikit-learn, and pandas.

Relevant files:

- `validate.py` — validates the contribution dataset.
- `train.py` — trains the intent classifier.
- `evaluate.py` — evaluates the trained model.
- `mobile_app.py` — runs the custom web demo (uses Python's standard HTTP server).
- `core.py` — contains shared project functionality.
- `requirements.txt` — lists Python dependencies.

Clone the repository:

```bash
git clone https://github.com/syd-xo/DataBuddies.git
cd DataBuddies
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the dataset:

```bash
python validate.py --track intent --data data/contribution.csv
```

Train the model:

```bash
python train.py --track intent --data data/contribution.csv
```

Evaluate the model:

```bash
python evaluate.py --track intent --data data/contribution.csv
```

Launch the demo:

```bash
python mobile_app.py
```

Once running, open `http://127.0.0.1:8501` in your web browser.

Evaluation outputs are written under `artifacts/intent/`:

- `test_metrics.json`
- `per_label_report.csv`
- `test_predictions.csv`

Run the training and evaluation commands to reproduce the model and its evaluation outputs.

## Results and limitations

The model achieved the following results on the 50-record test set:

| Metric | Result |
|---|---:|
| Accuracy | 0.90 |
| Macro-F1 | 0.8992 |
| Majority baseline accuracy | 0.10 |
| Majority baseline Macro-F1 | 0.0182 |

The model correctly classified 45 of the 50 test records. The majority baseline predicted `alarm_set` for every record and correctly classified 5 of 50.

The five observed test errors were:

| Record ID | Expected intent | Predicted intent |
|---|---|---|
| `LG-WEA-021` | `weather_query` | `news_query` |
| `LG-DAT-024` | `datetime_query` | `news_query` |
| `LG-CAL-022_2` | `calendar_query` | `calendar_set` |
| `LG-LIS-023_2` | `lists_query` | `lists_createoradd` |
| `LG-LIS-024_2` | `lists_query` | `lists_createoradd` |

The two list-related errors involve distinguishing requests to view a list from requests to create or add to one. The calendar error involves distinguishing a calendar lookup from a calendar event-creation request. These are possible interpretations of the observed errors, not confirmed explanations of the model's internal decisions.

Evaluation files:

- Overall test metrics: `artifacts/intent/test_metrics.json`
- Per-label results: `artifacts/intent/per_label_report.csv`
- Test predictions: `artifacts/intent/test_predictions.csv`
- Quality report and error analysis: `docs/QUALITY.md`

The dataset is relatively small, with only 25 examples per intent. The results therefore should not be treated as proof of performance across all Luganda speakers, dialects or real-world settings. The character-level model may also confuse intents with similar wording. The demo is a prototype: its responses are illustrative and it does not execute real-world actions. Its displayed probabilities are not calibrated, and it always predicts one of the 10 available intents.

## Presentation and demo video

- **Presentation/demo video URL (REQUIRED):** `https://youtu.be/PAHOlETQBy0`

The presentation should introduce the idea and approach, demonstrate the trained model with new input, discuss the evaluation results and limitations, and explain each member's contribution. The video must be accessible to the judges.

## Required materials

- **Contribution dataset and splits:** `data/contribution.csv`
- **Annotation guide:** `docs/ANNOTATION_GUIDE.md`
- **Source log and source terms:** `docs/SOURCE_LOG.md`
- **Dataset card:** `docs/DATA_CARD.md`
- **Quality/review report:** `docs/QUALITY.md`
- **Contribution and AI-use statement:** `docs/CONTRIBUTIONS.md`
- **Evaluation outputs and baseline comparison:** `artifacts/intent/test_metrics.json`, `artifacts/intent/per_label_report.csv`, `artifacts/intent/test_predictions.csv`, and `docs/QUALITY.md`
- **Runnable code and dependency file:** `validate.py`, `train.py`, `evaluate.py`, `mobile_app.py`, `core.py`, and `requirements.txt`
- **Trained artefacts or reproduction instructions:** Run `train.py` and `evaluate.py` as described above.
- **Video link:** `https://youtu.be/PAHOlETQBy0`

## Attribution and permissions

The project uses the provided starter kit structure and the MASSIVE-aligned intent label schema. The team's original code is released under the MIT License.

The contribution dataset contains original team-authored Luganda utterances. The data permission status is recorded as `documented_contributor_permission`, with written permission evidence retained privately rather than published in the repository.

ChatGPT was used to assist with drafting and structuring project documentation. The 250 Luganda utterances were authored by the team and were not generated by AI. The starter kit's example data and other upstream materials are not counted as original team contributions.