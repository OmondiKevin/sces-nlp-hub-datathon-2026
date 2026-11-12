# Dataset card: Team 10 Kikuyu cafeteria sentiment

**File:** `data/contribution.csv`  **Language:** Kikuyu (`ki`)  **Task:** 3-class sentiment (campus cafeteria).

| Label | Rows |
|---|---|
| positive | 110 |
| negative | 107 |
| neutral | 108 |
| **Total** | **325** |

**Splits (seed 10):** train 205 / dev 60 / test 60 (20 per label in dev and test).
**Provenance:** English source text written by Claude (AI), translated and adapted to Kikuyu by one team member. `source_method = human_localised`, `source_dataset = claude_generated_english_v1`. English text is not distributed.
**Review status:** 67 rows `independently_reviewed` (reviewer code `T10-R1`, a Kikuyu-speaking family member of a team member), 258 rows `self_reviewed`. All 60 test rows are independently reviewed. 5 rows were dropped by the reviewer (`data/exclusion_log.csv`); 33 rows carry her reworded version.
**Personal data:** none. Contributor and reviewer fields are pseudonymous codes.
**Intended use:** research and a teaching demo of a small baseline. **Not for:** deployment or as a general Kikuyu sentiment benchmark.
**Known limitations:** synthetic origin (translation of AI-written text); one translator and one reviewer; reviewer rewordings were mostly typed without diacritics, so orthography is mixed; only 72 rows were reviewed; small size; one domain.
**Licence / permission:** team contribution under the team's documented permission; code from the starter kit is MIT.
