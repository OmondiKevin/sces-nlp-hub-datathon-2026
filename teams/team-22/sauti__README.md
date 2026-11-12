# Sauti — Kiswahili semantic-parsing demo

**Live demo:** [Open Sauti](https://sauti.jollyground-e681768c.centralindia.azurecontainerapps.io/)

Sauti accepts a typed Kiswahili request and displays a short explanation of
the predicted Track C action and extracted slots. Expand **Maelezo ya modeli**
to inspect the JSON frame. The interface demonstrates parsing; it does not set
alarms, change calendars, retrieve weather or news, or answer factual
questions. Slot offsets are zero-based Unicode character positions with an
exclusive `end`.

## Model

The final model was trained on `Team_22_Dataset_Track_C.csv` with the ten
Track C action labels and five slot types. Its frozen-test results are
documented in
[`../docs/model/MODEL_EVALUATION_PROTOCOL.md`](../docs/model/MODEL_EVALUATION_PROTOCOL.md).
The app validates the metadata and rejects legacy label schemas.

The checkpoint is approximately 500 MB and is not stored in Git. Keep
`best_model.pt` beside its matching `metrics_and_errors.json` in
`models/track_c_final/`. The local model directory is ignored by Git.

## Run in Google Colab

Use the cell-by-cell workflow in
[`../docs/model/COLAB_TRACK_C_RUN.md`](../docs/model/COLAB_TRACK_C_RUN.md).
Cell 8 opens Sauti in the training runtime. Cell 9 loads the final checkpoint
and matching metadata from the shared run folder in a fresh runtime without
retraining.

## Run locally

From the project root, install Python 3.11+ dependencies and a PyTorch build
compatible with the hardware:

```powershell
python -m pip install -r requirements-model.txt
python sauti/sauti.py --repo . --checkpoint models/track_c_final/best_model.pt
```

Open <http://127.0.0.1:8000/>. The first run downloads AfriBERTa configuration
and tokenizer files from Hugging Face. The matching
`models/track_c_final/metrics_and_errors.json` must be present for Track C
schema validation.

## Output contract

Each response contains a Kiswahili explanation and, when available, a frame
with one `intent` and a list of typed slots. A low-confidence calendar
prediction may return two selectable choices. Corrections for a small set of
common misspellings are applied before inference while reported spans still
refer to the original request text.

The frame is a prediction, not a guaranteed interpretation or an executed
action. Test metrics and known error examples are documented in the evaluation
protocol.
