# Quality report

- **Team / language / version:** Team 19, Kiswahili (`sw-KE`), v1.0.
- **Accepted contributions by method and intent:** {'original_human': 250}; per label see the table below.

| Label | train | dev | test | total |
|---|---|---|---|---|
| weather_query | 15 | 5 | 5 | 25 |
| datetime_query | 15 | 5 | 5 | 25 |
| alarm_set | 15 | 5 | 5 | 25 |
| calendar_set | 15 | 5 | 5 | 25 |
| calendar_query | 15 | 5 | 5 | 25 |
| lists_createoradd | 15 | 5 | 5 | 25 |
| lists_query | 15 | 5 | 5 | 25 |
| play_music | 15 | 5 | 5 | 25 |
| news_query | 15 | 5 | 5 | 25 |
| qa_definition | 15 | 5 | 5 | 25 |

- **Unchanged external rows:** none.
- **Review counts:** {'self_reviewed': 200, 'independently_reviewed': 50}. Every test item: independently_reviewed.
- **Review of the first draft (250 records):** each record was checked against the label boundaries. 83 rows did not express their label (or were empty/duplicate) and were rewritten by team members; 11 had spelling/formatting fixed. Main problems found: calendar_set rows were mostly date questions; alarm_set and play_music rows included complaints and out-of-scope actions (volume, snooze, ringtone, skip); several news_query rows were comments, not requests.
- **Disagreements and resolutions:** where the review said a sentence did not express its label (e.g. a date question filed as calendar_set), the writers rewrote it rather than relabelling, to keep 25 sentences per intent; one duplicate created during rewriting (T19-SW-064/065) was replaced by a new sentence.
- **Duplicates / exclusions / missing fields:** 2 duplicates and 2 empty rows removed; the validator checks for duplicate text after normalisation and empty fields.
- **Groups and splits:** each record is its own group; relabelled rows kept their original split. Validator confirms no group crosses splits and every split has every label.
- **Model:** see README Results
- **Error analysis:** see README "Results and limitations".
- **Unresolved:** the rewritten rows are more formal than the first draft, so the data under-represents Sheng; per-sentence writer (Harry vs Michael) is not recorded, so train/dev rows are marked self_reviewed under the shared code T19-TEAM.
