# Team 22 | Sauti: Kiswahili limited semantic parsing

## Team and task

- **Team:** 22 (Kiswahili 3)
- **Members:** Gift Githaka Gicheru — Sauti interface; Brian Terer — model training and evaluation; Nyawita Elsie Damar — dataset, annotation, and provenance.
- **Language:** Kiswahili
- **Track:** C — limited semantic parsing
- **Original team repository:** [xtenders-nlp-datathon](https://github.com/xtensionlabs/xtenders-nlp-datathon)
- **Full source commit SHA for the version submitted:** `42f0bd0d31448235462da8a3bdc2ac5315a86939`. [`submission_snapshot_manifest.json`](submission_snapshot_manifest.json) lists checksums for the exact files included in this package.
- **Training source commit (full SHA):** `1a14618954ed9b3394c033e5b907fd7f8b344052`. The run manifest's training-script SHA-256 matches the script at this commit; the checkpoint SHA-256 also matches the saved checkpoint.

## Idea and approach

Sauti parses a typed Kiswahili request into one of the ten Track C actions and extracts exact character spans for dates, times, locations, items, and topics. Its browser interface explains the predicted action in Kiswahili and displays the structured frame. It demonstrates semantic parsing; it does not execute calendar or alarm actions, retrieve weather or news, or answer factual questions.

The team authored 250 requests, reviewed the action labels and slot spans with an independent Kiswahili reviewer, and used a fixed 15/5/5 split per action. A joint AfriBERTa intent and slot model with a constrained linear-chain CRF was selected on validation data and evaluated on the frozen test split. Train-only majority-intent and character TF-IDF baselines were measured on that same test split. Sauti presents the output in a browser with a short Kiswahili explanation and inspectable JSON.

## Data and review

The sole contribution dataset has 250 unique team-authored requests: 25 per action, with 150 train, 50 validation, and 50 test rows. It contains 475 slot annotations across five types; 239 requests have at least one slot. The test set contains 48 slot-bearing and two slot-free requests. The structural audit found no malformed slot JSON, unsupported slot types, invalid character offsets, or overlapping spans. An independent Kiswahili reviewer approved all 250 requests, labels, slots, and grouping. Fifty inherited labels were corrected to the handbook actions `lists_createoradd` and `qa_definition`; the accepted changes and reasons are logged.

The public source log records source, contribution, review, correction, and split information. Team-authored requests are authorized for this Datathon submission and assessment; no open-data licence is claimed. Private permission evidence and identity mappings are retained outside this public package. The public dataset replaces paths to that evidence with an opaque private record ID.

The final model run used dataset SHA-256 `0756d1b54581bd23eab36a0455e987e3ca6d45d51f61ab5f544d146058509193`. The submitted CSV has SHA-256 `0e10c800925e101af08aee1213f55543dcc508a024da918d6c87d3a96703835f`. Its permission reference is an opaque private record ID, and its adjudication notes use concise judge-facing wording. Requests, labels, slots, review statuses, and splits are identical, so no model input changed.

## Code and how to run

The upload files use double underscores in place of their original folder separators (for example, `docs__data__dataset_card.md`). The complete directory layout is preserved in [`team-22-source.zip`](team-22-source.zip), which is the convenient download for running the application or training workflow.

The package includes the dataset audit, model training and evaluation scripts, baseline evaluation, Sauti browser app, documentation, provenance logs, and machine-readable evaluation outputs. It targets Python 3.11 or newer. Install model dependencies from this directory:

```bash
python -m pip install -r requirements-model.txt
python audit_track_c.py Team_22_Dataset_Track_C.csv
python evaluate_track_c_baselines.py --data Team_22_Dataset_Track_C.csv --output-dir results/track_c_baselines
```

The complete Google Colab sequence for validation selection, final training, frozen-test evaluation, artifact backup, and the Sauti interface is in [`docs/model/COLAB_TRACK_C_RUN.md`](docs__model__COLAB_TRACK_C_RUN.md). Training uses `castorini/afriberta_large`, seed 42, and a CUDA GPU. The final checkpoint is approximately 500 MB and is not included in Git; the evaluation metadata is included at [`models/track_c_final/metrics_and_errors.json`](models__track_c_final__metrics_and_errors.json). Reproduce the checkpoint with the Colab workflow. The matching `best_model.pt` must be placed beside that metadata to run Sauti locally.

## Results and limitations

The final AfriBERTa joint model used seed 42 and selected epoch 8 on validation. The frozen test set contains 50 requests, five per action. Its run manifest, validation outputs, label mappings, test predictions, and metrics are included under [`models__track_c_final__run_manifest.json`](models__track_c_final__run_manifest.json).

| System | Intent accuracy | Intent macro-F1 | Exact slot F1 | Full-frame exact match | JSON validity | Unseen-value exact recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AfriBERTa joint model | 100.00% | 100.00% | 79.01% | 58.00% | 100.00% | 58.33% |
| Character TF-IDF + train-only surface matcher | 86.00% | 85.65% | 56.52% | 24.00% | 100.00% | 0.00% |
| Character TF-IDF, empty slots | 86.00% | 85.65% | 0.00% | 4.00% | 100.00% | 0.00% |

Detailed per-label metrics, the baseline outputs, metric definitions, and five actual test errors are linked in [`docs/model/MODEL_EVALUATION_PROTOCOL.md`](docs__model__MODEL_EVALUATION_PROTOCOL.md) and [`results__track_c_baselines__baseline_metrics.json`](results__track_c_baselines__baseline_metrics.json). The model's intent result is strong on this split, but its 58.00% full-frame exact match and 58.33% unseen-value recall show that slot extraction remains a challenge. The test set is small and was reselected from former training examples after the earlier test split had been used during development; it is not a prospective sample. Sauti displays a prediction and does not carry out the requested action.

## Presentation and demo video

**Hosted app:** [Open Sauti live demo](https://sauti.jollyground-e681768c.centralindia.azurecontainerapps.io/)

**Presentation and demo video:** [Watch the Team 22 Sauti demo](https://drive.google.com/file/d/15205PpFJ1IsgqgwVJjbXi9bssGKrvZhE/view)

The video demonstrates Sauti on new Kiswahili input and reports the measured results and limitations. The hosted app link accompanies the video.

## Required materials

- Contribution dataset and splits: [`Team_22_Dataset_Track_C.csv`](Team_22_Dataset_Track_C.csv)
- Annotation guide: [`docs/data/annotation_guide.md`](docs__data__annotation_guide.md)
- Source log, correction log, and split record: [`provenance__README.md`](provenance__README.md)
- Dataset card: [`docs/data/dataset_card.md`](docs__data__dataset_card.md)
- Quality and review report: [`docs/data/quality_report.md`](docs__data__quality_report.md)
- Contribution and AI-use statement: [`docs/team/contribution_and_ai_use.md`](docs__team__contribution_and_ai_use.md)
- Final test predictions, per-label metrics, test errors, and run manifest: [`models/track_c_final/test_predictions.json`](models__track_c_final__test_predictions.json), [`models/track_c_final/metrics_and_errors.json`](models__track_c_final__metrics_and_errors.json), and [`models/track_c_final/run_manifest.json`](models__track_c_final__run_manifest.json)
- Validation metrics and predictions, and label mappings: [`models/track_c_final/validation_metrics.json`](models__track_c_final__validation_metrics.json), [`models/track_c_final/validation_predictions.json`](models__track_c_final__validation_predictions.json), and [`models/track_c_final/label_mappings.json`](models__track_c_final__label_mappings.json)
- Evaluation protocol and metric definitions: [`docs/model/MODEL_EVALUATION_PROTOCOL.md`](docs__model__MODEL_EVALUATION_PROTOCOL.md)
- Baseline outputs: [`results__track_c_baselines__baseline_metrics.json`](results__track_c_baselines__baseline_metrics.json)
- Runnable code and dependencies: [`team-22-source.zip`](team-22-source.zip), [`requirements-model.txt`](requirements-model.txt), and [`docs/model/COLAB_TRACK_C_RUN.md`](docs__model__COLAB_TRACK_C_RUN.md)
- Hosted app: [Sauti live demo](https://sauti.jollyground-e681768c.centralindia.azurecontainerapps.io/)
- Presentation/demo video: [Watch the Team 22 Sauti demo](https://drive.google.com/file/d/15205PpFJ1IsgqgwVJjbXi9bssGKrvZhE/view)
- Trained artifact instructions: [`docs/model/COLAB_TRACK_C_RUN.md`](docs__model__COLAB_TRACK_C_RUN.md)
- Submission snapshot file hashes: [`submission_snapshot_manifest.json`](submission_snapshot_manifest.json)

## Attribution and permissions

The task schema follows the Strathmore NLP Hub Datathon Handbook and [Starter Kit v2](https://drive.google.com/file/d/1OTDqXGAWxq9Kf7mTFLmu4rjzcYMzKlqQ/view). The model uses the pretrained [`castorini/afriberta_large`](https://huggingface.co/castorini/afriberta_large) checkpoint, whose model card identifies the model as MIT licensed. The AfriBERTa paper is [Ogueji, Zhu, and Lin (2021)](https://aclanthology.org/2021.mrl-1.11/). Team-authored requests are used under permission for Datathon submission and assessment; they are not released under an open-data licence. The project code has no separate open-source licence claim. AI assistance and human review are described in [`docs/team/contribution_and_ai_use.md`](docs__team__contribution_and_ai_use.md).
