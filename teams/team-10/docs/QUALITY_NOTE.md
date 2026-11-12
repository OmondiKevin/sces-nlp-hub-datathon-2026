# Quality note: Team 10

## What was checked
- Automatic: unmodified `validate.py` passes (no duplicates, no blanks, label balance, every split has every label, every test row independently reviewed, reviewer differs from author).
- Author: one translator produced and re-read all rows.
- Independent review: a Kikuyu-speaking family member of a team member (reviewer code `T10-R1`) checked a random sample of 72 rows (24 per label) with OK / FIX / DROP verdicts: 32 OK, 35 FIX, 5 DROP. DROP rows were removed (`data/exclusion_log.csv`). In 2 FIX rows only diacritics/spacing differed, so the original text was kept; in 33 rows her rewording was adopted (whitespace normalised).

## What was NOT done
- Only 72 of the original 330 rows were reviewed; 258 remain `self_reviewed`, including most training rows.
- The two teammates asked to review could not be reached before the deadline.
- Her rewordings were mostly typed without diacritics (ĩ, ũ), and we did not check that each reworded sentence still has its original label. Orthography in the data is therefore mixed.
- Single reviewer, so no agreement statistic.

## Results (test set evaluated once, after settings were frozen)
| | Accuracy | Macro-F1 | Majority baseline macro-F1 |
|---|---|---|---|
| Dev (60) | 0.750 | 0.739 | 0.167 |
| Test (60) | 0.683 | 0.640 | 0.167 |

Test per-label recall: positive 0.95, negative 0.25, neutral 0.85 (19 of 60 rows wrong). Five real errors are listed in the README; a Kikuyu speaker should check them.

## Known risks
- The handbook asks for natural Kikuyu written by speakers. Ours is a human translation of AI-written English, so it may differ from spontaneous speech.
- The test set is small (60 rows); scores vary with the split. No minimum score is claimed.
- Negative opinions are poorly detected by this baseline.
