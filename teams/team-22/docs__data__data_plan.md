# Team 22 data plan

## Declaration

- **Team:** 22, Kiswahili 3
- **Track:** C, limited semantic parsing
- **Language:** Kiswahili, reviewed by an independent Kiswahili reviewer.
- **Output:** one exact handbook action label plus zero or more text spans of
  type `location`, `date`, `time`, `item`, or `term`.

## Dataset

`Team_22_Dataset_Track_C.csv` is the only dataset CSV. It has 250 rows, exactly
25 per Track C action, with 15/5/5 train/validation/test splits. It contains
224 inherited team-authored examples, including 50 reviewer-approved label
corrections, and 26 additional team-authored requests. Twenty-six
programmatic-padding records from older drafts are excluded.

An independent Kiswahili reviewer approved all 250 records, including
language, labels, slots, and grouping. Every row is marked
`independently_reviewed`. The additional requests use contributor code
`T22-AUTH-01` and reviewer code `T22-R1`; inherited rows retain source
reviewer code `member_A`.

## Annotation and split plan

The ten labels are the exact Track C actions in the handbook. The 25 additional
`lists_query` examples are split 15/5/5. One additional `calendar_set` request
fills that action's split to 15/5/5. The dataset has 475 slot annotations,
239 slot-bearing records, and 338 distinct exact slot type/value pairs. All
five slot types occur, with both slot-bearing and slot-free test requests.

Slot offsets are zero-based Python Unicode character positions with exclusive
`end`; each slot must satisfy `text[start:end] == value`. The structural audit
finds no invalid JSON, unsupported slot types, invalid offsets, or overlapping
spans. The audit reports per-action slot-value diversity and 51 exact test
slot values absent from training. The former test split was used during model
development, so five records per action were selected from the former training
rows for the new test; the old test rows moved to training. This preserves
15/5/5 and is recorded in `../../provenance/track_c_split_reassignment.json`.

## Sources, rights, and release

`../../provenance/Team_22_Source_Log.csv` records source IDs, versions, URLs, methods, permission
references, contributor/reviewer codes, review statuses, splits, and label
corrections for all 250 rows. `../../provenance/track_c_label_correction_log.csv` preserves
original and accepted labels for the 50 corrected records.

Team 22 authorized use for this Datathon submission, judging, evaluation, and
demonstration. This does not grant open redistribution, commercial use, or
reuse outside this project. The source log references private permission
record `T22-PERM-2026-11-11`; supporting evidence and identity mappings are
retained outside the public submission. No open license is claimed.

The final AfriBERTa model used the requests, labels, slots, and splits in
`Team_22_Dataset_Track_C.csv`. The public CSV uses an opaque permission-record
ID and concise, judge-facing adjudication notes instead of a path to private
evidence and an internal confirmation note. These metadata edits did not change
model inputs. The model's
frozen-test results, train-only baseline comparison, and error analysis are in
`../model/MODEL_EVALUATION_PROTOCOL.md`. See `quality_report.md` and
`../../provenance/Team_22_Source_Log.csv` for the structural audit and
row-level provenance.
