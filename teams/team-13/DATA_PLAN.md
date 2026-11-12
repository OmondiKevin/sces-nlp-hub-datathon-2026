# Completed data and experiment plan

Track A; primary language Kikuyu (ki); ten organiser intents. Use team-supplied human-authored A1/A2/A3 material with team-confirmed datathon use/sharing permission and independent fluent R1/R2/R3 review. Details are in DATA_CARD.md and row logs. No synthetic data substitutes for human contribution.

Import 330 reviewed records verbatim. Keep glosses separate. Validate nonempty required metadata, label coverage, exact-normalised duplicates, reviewer/author distinction, split sizes and group isolation. Keep lexical families at similarity >=0.85 together. Reserve five new extension records per label as a fresh test; five original-pool records per label as dev; the other 23 as train. Split assignment is deterministic and uses no model outputs.

Use the fixed baseline extracted from the user's current Colab, freeze before evaluation, then compare the final candidate and original 250 model on the same new holdout once. Preserve historical results as separate evidence. Publish permitted data, actual predictions/errors, hashes, runnable code, public demo and backup recording. The separate 330 run does not alter any text in the user's live Colab. Actual results and caveats are in README.md and QUALITY.md.
