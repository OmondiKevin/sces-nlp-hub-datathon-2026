# Dataset card and source log

**Team, primary language, variety, version and date:** Team name 14 (Maa). Maasai (Maa), language code `mas`. Contributors gave their Maa section or area: Kaputiei (10), Kajiado (5), Purko (4), Matapato (3), Kisongo/Ilkisongo (3), Narok (2), Loodokilani (2), and one each from Kimana, Ildalat-le-kutuk, Laikipiak, Keekonyokie, Ildamat, Loitoktok and Moitanik. Five did not name one ("all" or "Masai"). Version `2026-11`, built 11 November 2026.

**Task and intended use:** Intent classification of short spoken-style requests to a phone assistant, written in Maa. There are 10 labels: weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query and qa_definition. The data is for research and teaching, and for building a baseline Maa assistant.

**Data fields, counts and splits:** The starter kit's 15 columns (`record_id` … `split`). There are 1,024 records, split into 687 train, 172 dev and 165 test.

| Label | Train | Dev | Test | Total |
|---|---|---|---|---|
| weather_query | 70 | 18 | 19 | 107 |
| datetime_query | 66 | 17 | 16 | 99 |
| alarm_set | 78 | 20 | 18 | 116 |
| calendar_set | 72 | 16 | 15 | 103 |
| calendar_query | 75 | 18 | 16 | 109 |
| lists_createoradd | 68 | 16 | 16 | 100 |
| lists_query | 62 | 17 | 18 | 97 |
| play_music | 59 | 16 | 15 | 90 |
| news_query | 67 | 17 | 16 | 100 |
| qa_definition | 70 | 17 | 16 | 103 |

**Sources:** There is no external dataset. All the text was newly written by 41 Maa speakers in the team's Google Form "How would you say it in Maa", between 9 and 11 November 2026. `source_dataset` = `team_maa_intent_google_form`, `source_method` = `original_human`, `source_url` = `not_applicable`. Licence: CC-BY-4.0, with contributor consent recorded in the form. Transformations: the metadata columns were removed, along with blanks, duplicates and junk entries. The text was normalised. See QUALITY.md.

**Contributor permission for newly authored text:** Every one of the 41 respondents ticked "I am 18 or older, I have read the above, and I agree to take part." The form export with timestamps is held privately by the team and is not in this repository.

**Annotation and language-review process:** Labels come from the form design. Each of the 20 situations was written to match one intent, two situations per intent. Contributors wrote what they would say in each situation, and could give a second way of saying it. All the records, including every test record, were then checked by an independent Maa reviewer (code R01) who did not write them. See ANNOTATION_GUIDE.md.

**Known limitations and excluded uses:**
- The text is written, not transcribed speech.
- Spelling varies between speakers, because Maa has no single standard spelling in everyday use.
- Some sentences mix in Swahili or English words, such as *alarm*, *kalenda*, *biashara* and *habari*.
- Kaputiei and Kajiado speakers are over-represented.
- 4 contributors said they are not confident speaking Maa.
- Each sentence answers a given situation, so phrasing may be less varied than real use.
- Do not use this data to judge a speaker's fluency, or for any purpose beyond the 10 intents.

**Credit and correction contact:**Philip Tait (form administrator), through the official datathon event channel. Contact details are kept out of the repository.

   **Proposed release terms and pending decisions:** CC-BY-4.0 for the text, pending confirmation that the form's consent notice covers public release. Contributor names and the raw form export stay private.
