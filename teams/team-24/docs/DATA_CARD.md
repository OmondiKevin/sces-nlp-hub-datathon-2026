# Dataset card and source log — Team 24 (Kiswahili 5)

## Team, language, variety, version, date
Team 24 "Kiswahili 5". Kiswahili (`sw-KE`), everyday Kenyan Swahili, spoken-request register. Dataset version `v1`, 2026-11-11. File: `data/contribution.csv`.

## Task and intended use
Track A intent classification: 10 action labels (see `taxonomy.csv`). Intended use: the Strathmore NLP Hub Datathon 2026 — training and evaluating a small prototype classifier and demonstrating a simulated assistant. **Not** intended for production use, speech, translation, or general-purpose Kiswahili evaluation.

## Data fields, counts and splits
Fields: `record_id, language, text, label, source_dataset, source_version, source_record_id, source_url, source_method, licence_or_permission, contributor_code, reviewer_code, review_status, group_id, split`.

**262 rows: 159 train / 51 dev / 52 test.** Every label meets the 15 / 5 / 5 minimum:

| Label | Train | Dev | Test | Total |
|---|---|---|---|---|
| weather_query | 16 | 5 | 5 | 26 |
| datetime_query | 16 | 5 | 5 | 26 |
| alarm_set | 15 | 5 | 5 | 25 |
| calendar_set | 17 | 6 | 6 | 29 |
| calendar_query | 16 | 5 | 5 | 26 |
| lists_createoradd | 16 | 5 | 5 | 26 |
| lists_query | 16 | 5 | 5 | 26 |
| play_music | 15 | 5 | 6 | 26 |
| news_query | 16 | 5 | 5 | 26 |
| qa_definition | 16 | 5 | 5 | 26 |

Every row has its own `group_id` (no shared sources or paraphrase groups).

## Sources (source log)
| Source | Rows | Status | Notes |
|---|---|---|---|
| Team-authored text (`team_authored`, `original_human`) | 262 | **In dataset** | Written by team members from everyday situations. Contributor codes 24K and 24N. |
| `Rogendo/Eng-Swa-Dataset`, file `swa.txt` — https://github.com/Rogendo/Eng-Swa-Dataset | 110 (record IDs 24-262 to 24-371) | **Excluded; not used for training, evaluation or counts** | No licence (GitHub API `license: null`, no LICENSE file; the Hugging Face mirror has no licence tag and an empty card), no stated provenance ("English and translated Swahili sentences"). Most rows also did not fit any of the 10 intents. Repo created 2023-05-13. The excluded rows are not republished here. |
| Organiser starter kit v2.0 (code, templates, practice sets) | 0 contribution rows | Reused code, credited | Code under the kit's `LICENSE_CODE.txt`. English practice fixtures were used only for the practice run. |
| MASSIVE, AfriSenti, Common Voice | 0 | Not used | MASSIVE's label schema is followed via the organiser's taxonomy. |

## Contributor permission for newly authored text
Text was written by the team for the datathon and recorded as "Written by the team for the Datathon". Permission evidence is held separately by the team and is not in this repository. 

## Transformations after first drafting (all logged)
- 7 rows reworded because they did not match their intent; 8 rows reworded to make the intent unambiguous; 7 further rows reworded after a pre-review check (24-077 was reworded twice). 21 distinct rows in total.
- 11 spelling/grammar corrections; 5 rows changed from *alarm* to *kengele*; 3 rows relabelled `alarm_set` → `calendar_set`; 2 rows moved train → test to meet the per-label minimum; 2 new rows added (24-372, 24-373); 1 spelling fix (*redio*).
- **Wording for 35 rows was suggested or drafted by an AI assistant, then approved by team members** (33 existing rows plus the 2 new rows, whose final text was written by the team from a draft). The CSV records all rows as `original_human`; this limitation is stated in CONTRIBUTIONS.md. 

## Annotation and language-review process
See ANNOTATION_GUIDE.md and QUALITY.md. Test rows: 43 reviewed by Moses (24M), 9 by Nathan (24N). Train/dev rows are recorded as reviewed by 24M on 2026-11-11. The validator passes, but it cannot check fluency or rights.

## Known limitations and excluded uses
- Small: 262 rows, **5–6 test rows per label**, so one error moves scores a lot.
- One language variety, a handful of authors, written situations rather than real user logs.
- The model reads topic words more than request type (see QUALITY.md errors); real assistants would see wider phrasing.
- Informal forms and a few loanwords are kept; they may not match other Kenyan or Tanzanian varieties.
- Not suitable for sentiment, NER, translation or speech work; not evidence about other languages.
- All three team members state they are fluent in Kiswahili; fluency was not independently certified.

## Credit and correction contact
Team 24, Kiswahili 5 (Moses, Krysia, Nathan). Corrections can be sent to the team by WhatsApp or email.

## Proposed release terms and pending decisions
- **Use:** the organisers may add the 262 accepted rows to the combined NLP Hub corpus.
- **Credit:** Team 24 (Kiswahili 5) is named as the source.
- **Licence:** the team has not chosen a licence for the text and will follow the organisers' terms once announced.

Code licence follows the organiser kit.
