# Dataset provenance

These records accompany `Team_22_Dataset_Track_C.csv`; they are not
additional datasets.

- `Team_22_Source_Log.csv`: one source, review, permission-reference, and split
  record per example.
- `track_c_label_correction_log.csv`: the original and accepted labels,
  reasons, and reviewer codes for 50 corrections.
- `track_c_split_reassignment.json`: deterministic assignment of the current
  15/5/5 splits.

Contributor and reviewer values are pseudonymous codes. Permission references
identify records held outside the public submission; the audit checks their
presence and format but cannot determine legal scope.

Where the original reviewer date was not recorded, `review_date` retains the
value `not_recorded`; the adjudication note records when approval was confirmed
for the public provenance log.
