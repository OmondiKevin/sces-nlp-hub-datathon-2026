# Track C model evaluation protocol

## Frozen data split

The original 50-row test split was used to compare model experiments. To keep a
final report from reusing those test outcomes, `reassign_track_c_splits.py`
created a new 50-row test split from five former training records per intent.
The former test rows moved to training; validation stayed fixed. The operation
changed no sentence, label, slot, or review field. It kept the authoritative
dataset at exactly 250 rows with 15 train, 5 validation, and 5 test records per
intent. The row-level split changes are recorded in
`../../provenance/track_c_split_reassignment.json`, and
`../../provenance/Team_22_Source_Log.csv` was updated to
match.

The new test records were not evaluated in the previous experiment. The
retired checkpoint had included them in training, so the final run started from
pretrained AfriBERTa and used only the current `train` split. This is a fresh
holdout for this run, with a small-data limitation: the records were not newly
collected utterances. A completely prospective test would require additional
reviewed records.

Validation is the model-selection split. The `--validation-only` option saves
validation metrics and predictions without evaluating test; the final test
evaluation was run once after code, data, and settings were frozen. Test results
were used only for reporting. A model change based on these errors would make a
later score exploratory unless a new holdout were reserved.

## Required measurements

`track_c_evaluation.py` reports:

- Intent accuracy, macro-F1, per-label precision/recall/F1, and a confusion
  matrix.
- Micro slot precision/recall/F1 using an exact `(slot type, start, end)` match
  over Unicode character offsets.
- Full-frame exact match, requiring the correct intent and the complete exact
  slot set.
- JSON validity after serialization, with schema, allowed slot types, offsets,
  and `text[start:end] == value` checked.
- Unseen slot-value counts and exact recovery/error details. A test value is
  considered seen only if the same normalized `(type, value)` occurs in the
  training annotations.
- All per-record predictions and up to five actual errors (all errors when
  fewer than five occur).

The model checkpoint is selected using validation full-frame exact match,
breaking ties by intent macro-F1 and then exact-span slot F1. Test results do
not participate in checkpoint selection.

## Baselines

Run `evaluate_track_c_baselines.py` on the same preset split. It fits only on
the train rows and records:

- A majority-intent comparator.
- Character TF-IDF (2–5 grams) with logistic regression for intent.
- The same intent model with an empty slot set.
- The same intent model plus a longest-match surface-value slot matcher built
  only from training annotations.

Each system is scored with the same intent, exact-slot, frame, JSON, and unseen
value metrics. The output includes overall metrics, per-label F1, confusion
matrices, predictions, and up to five errors.

The baselines have been run on the revised test set. Character TF-IDF plus
logistic regression scored 0.8565 intent macro-F1. Adding the train-only
surface matcher scored 0.7647 slot precision, 0.4483 recall, 0.5652 F1, and
0.2400 full-frame exact match. The TF-IDF empty-slot comparator scored 0.0400
full-frame exact match. The majority-intent macro-F1 is 0.0182. Full results
are in `results/track_c_baselines/`.

The fixed test contains five examples per action. Treat these as prototype
estimates, report the per-action counts and errors, and avoid presenting them
as broad claims about Kiswahili performance.

## Final Colab result

The final run used `castorini/afriberta_large`, seed 42, and selected epoch 8.
On the frozen 50-row test set it scored 1.0000 intent accuracy and macro-F1,
0.8533 exact-slot precision, 0.7356 recall, 0.7901 F1, 0.5800 full-frame exact
match, 1.0000 JSON/schema validity, and 0.5833 unseen-value exact recall. The
test dataset SHA-256 was
`0756d1b54581bd23eab36a0455e987e3ca6d45d51f61ab5f544d146058509193`.

The public submission dataset uses the same requests, labels, slots, review
statuses, and splits. Its permission reference is an opaque private record ID
(`T22-PERM-2026-11-11`), and its adjudication notes use concise judge-facing
wording. Its SHA-256 is
`0e10c800925e101af08aee1213f55543dcc508a024da918d6c87d3a96703835f`. These
metadata-only edits protect permission evidence and do not alter model inputs.

The model exceeds the strongest train-only baseline by 14 percentage points
in intent accuracy, 22.49 points in exact-slot F1, and 34 points in full-frame
exact match. The test has only five examples per action and was selected from
former training rows, not newly collected utterances. Report the scores with
that limitation, the per-record predictions, and up to five actual errors.

The recorded test error analysis contains five full-frame mistakes:

| Record | Gold frame detail | Model error |
| --- | --- | --- |
| `rec_028` | Calendar query with item `shughuli` and date `wiki hii`. | Correct intent and date; missed the item. |
| `rec_055` | Calendar set with item `sherehe ya kuzaliwa`, date, and time. | Correct intent, date, and time; missed the item. |
| `rec_083` | Date/time query with time `Saa 07:45`. | Correct intent and time; added a false `location` span for `Kiswahili`. |
| `rec_106` | Definition query with term `afya bora`. | Correct intent; returned only `afya` as the term. |
| `rec_153` | News query with terms `Gor Mahia` and `mechi yao ya kirafiki`. | Correct intent and first term; missed the second term. |

## Colab run

Use the cell-by-cell instructions in [`COLAB_TRACK_C_RUN.md`](COLAB_TRACK_C_RUN.md).
They clone or fast-forward `main`, stop if the current Track C files are missing,
run train-only baselines and three validation-only ablations, select one
configuration without test metrics, then run the final test comparison once.

The complete `/content/track_c_final` run folder contains the checkpoint,
`metrics_and_errors.json`, `test_predictions.json`, `label_mappings.json`,
`validation_metrics.json`, `validation_predictions.json`, `run_manifest.json`,
and tokenizer. The manifest records data/code/checkpoint hashes, package
versions, split sizes, and run settings. The Colab artifact-backup cell also
copies the baseline output folder, three validation-only candidate folders,
and `validation_model_selection.md`.

Choose among the three variants using validation full-frame exact match,
breaking ties by intent macro-F1 and exact-span slot F1. If softmax/no
augmentation wins, use `--no-crf --no-slot-value-augmentation` for the final
run. If CRF/no augmentation wins, use `--use-crf --no-slot-value-augmentation`.
If CRF plus augmentation wins, keep the command as written.
