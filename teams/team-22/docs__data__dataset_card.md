# Team 22 Track C dataset card

## Purpose

This dataset supports a Kiswahili limited semantic parser. Each request
receives one of the ten handbook action labels and zero or more exact text
spans for `location`, `date`, `time`, `item`, or `term`. It does not translate
requests, infer dates, execute actions, or provide factual answers.

## Version and status

- **Team:** 22, Kiswahili 3
- **Track:** C
- **Language:** Kiswahili, reviewed by an independent Kiswahili reviewer
- **Dataset file:** `Team_22_Dataset_Track_C.csv`
- **Status:** 250 reviewer-approved records, 25 per action, and 15/5/5
  train/validation/test splits. This is the only dataset CSV in the repository.

## Contents

- 224 inherited team-authored records; 50 have accepted label corrections.
- 26 additional team-authored requests: 25 `lists_query` and one
  `calendar_set`.
- 26 programmatic-padding records from older drafts are excluded.
- 475 slot annotations; 239 records contain at least one slot.
- Test has 48 slot-bearing and 2 slot-free requests. Train has 144 slot-bearing
  and 6 slot-free; validation has 47 slot-bearing and 3 slot-free.
- All 250 records are marked `independently_reviewed`. The audit reports zero
  malformed slot JSON, unsupported slot types, invalid character offsets, or
  overlapping spans.

## Action labels and splits

The dataset uses exactly the handbook labels:

`weather_query`, `datetime_query`, `alarm_set`, `calendar_set`,
`calendar_query`, `lists_createoradd`, `lists_query`, `play_music`,
`news_query`, and `qa_definition`.

Every class has 15 train, 5 validation, and 5 test examples. The 50 accepted
corrections map `take_note` to `lists_createoradd` and `general_qa` to
`qa_definition`. Original labels, corrected labels, reasons, and reviewer codes
are in `../../provenance/track_c_label_correction_log.csv`.

## Sources, permissions, and AI use

`../../provenance/Team_22_Source_Log.csv` records source IDs, versions, methods,
permission references, contributor/reviewer codes, review status, splits, and
correction details for all rows. Team 22 authorized use of the data for this
Datathon submission, judging, evaluation, and demonstration. This does not
grant open redistribution, commercial use, or reuse outside this project. No
CC0 or open license is claimed. Permission evidence and identity mappings are
retained privately and are not part of the public submission package.

The test split was reset after the former test results were used during model
development. Five former training records per action form the new test; the
former test records now belong to training. This preserves 15/5/5 and is
documented in `../model/MODEL_EVALUATION_PROTOCOL.md` and
`../../provenance/track_c_split_reassignment.json`.

The request texts were authored by Team 22. Codex-assisted slot annotation for the
26 additional requests and the rest of its contribution are disclosed in
`../team/contribution_and_ai_use.md`. The final AfriBERTa model used these
requests, labels, slots, and splits. The public CSV uses an opaque private
permission-record ID and concise adjudication notes; neither change affects
model input.
Frozen-test metrics and error analysis are documented in
`../model/MODEL_EVALUATION_PROTOCOL.md`.

See `../model/TRACK_C_EVIDENCE.md` for the judging evidence summary and
`quality_report.md` for the structural audit.
