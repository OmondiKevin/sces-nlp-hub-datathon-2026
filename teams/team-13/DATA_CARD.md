# Dataset card — Team 13 Kikuyu intent data

Task: Track A text intent classification, the ten fixed labels in taxonomy.csv. Primary language code ki, Kikuyu/Gikuyu. Dialect/variety and speaker demographics unspecified; do not infer them.

330 human-written records as attested by the team: A1/R1 100; A2/R2 100; A3/R3 50; A2/R3 DOCX extension 80. The team confirms authors permit datathon use and sharing and reviewers are fluent, independent non-authors of their batches. No public CC licence is asserted. Source/review logs retain row IDs and user-confirmation evidence. Actual review dates are unknown. Code licensing does not relicense data.

Each of ten labels has 33 records. New final split: 23 train, 5 dev, 5 test per label. The 50 test records all come from the new extension; it is a small one-author holdout. English glosses are reference-only and absent from training features. Original wording and assigned labels were preserved. No English practice data enters the final model.

NFC/casefold and whitespace duplicate checks passed. Lexical similarity >=0.85 connected families stay in one split; this does not detect all semantic paraphrases. Source text contains genuine spelling/code-switching variation as supplied. Review flags remain visible, not silently linguistically corrected. Intended use: educational prototype and auditable datathon evaluation. Not a representative or production-ready Kikuyu corpus. See QUALITY.md and EXPERIMENT_PROTOCOL.json for measured limitations.
