# Dataset card and source log

- **Team / language / version:** Team 19, Kiswahili (`sw-KE`), v1.0, 12 Nov 2026.
- **Task and intended use:** training and evaluating intent classifiers for Kiswahili phone-assistant requests (datathon prototype). Not for production use without more data.
- **Fields:** the 15 starter-kit columns (record_id, language, text, label, source_dataset, source_version, source_record_id, source_url, source_method, licence_or_permission, contributor_code, reviewer_code, review_status, group_id, split).
- **Counts:** 250 records.

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

- **Sources:** `team_authored`, newly written by Team 19 members (`original_human`). No downloaded or external dataset rows. Source URL: not_applicable.
- **Transformations:** whitespace/tab removal; 83 rows rewritten by team members after review and 11 corrected, all listed with reasons in `data/review_changes.csv` and reproducible with `team19_final.py`.
- **Contributor permission:** members agreed to the use of their sentences for the datathon; evidence held privately.
- **Annotation and review:** see `docs/ANNOTATION_GUIDE.md` and `docs/QUALITY.md`.
- **Limitations:** few writers, about 25 sentences per label, mostly short requests; regional variation is limited. Exclude uses that assume coverage of all Kiswahili varieties.
- **Credit / correction contact:** via the organiser channel.
- **Proposed release terms:** CC-BY-4.0.
