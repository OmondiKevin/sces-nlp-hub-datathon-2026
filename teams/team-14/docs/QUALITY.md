# Quality report

**Team / language / dataset version:** Team 14 (Maa) / Maasai (`mas`) / 2026-11

**Accepted contributions by source method and intent:** All 1,024 records are `original_human`. Per intent: weather_query 107, datetime_query 99, alarm_set 116, calendar_set 103, calendar_query 109, lists_createoradd 100, lists_query 97, play_music 90, news_query 100, qa_definition 103.

**Unchanged external training rows (not counted as contributions):** None.

**Independent review counts (including every test item):** 1,024 of 1,024 records are `independently_reviewed`, including all 165 test records. The reviewer (R01) is not the author of any record.

**Disagreements and resolutions:** The reviewer worked directly on the form export. Comparing the raw export with the reviewed one:
- The raw export had 1,247 non-empty sentence answers from 41 respondents, plus one stray row of label names, which was removed.
- **136 answers were deleted.** 105 of them were non-answers such as "No", "Yes", "N A", "pass" and "Not sure". These were mostly typed into the optional "another way" boxes. The other 31 were real attempts that did not fit their situation or label: an answer about news typed under weather, bare words such as *Taata* ("today") or *Jumaine*, half-English answers such as *Intarikini tomorrow*, and `____` placeholders.
- **124 answers were corrected.** The corrections fixed spelling and word breaks (*endama* to *e dama*, *Kaaolong* to *Kaa olong*, *inatumo* to *ina tumo*, *ntanekini* to *ntarekini*), removed emoji and English notes such as "(3pm)" and "(Tuesday 4th December)", and fixed autocorrect damage (*Toyshop oltwala* to *Tosho oltwala*, *Enjoy eishir* to *Echoo eishir*).
- No answer was moved to a different intent.

The reviewer's version (1,111 answers) is the input to the cleaning step described below.

**Duplicates / exclusions / missing fields:** After review there were 1,111 non-empty sentences from 41 respondents (20 situations, each with a main answer and an optional second way of saying it). We removed:
- 68 duplicates. Two sentences counted as duplicates if they matched after ignoring case, punctuation and spacing. Many speakers gave the same short answer, such as *Kesaaja?*. We kept the first and dropped the rest, so the same sentence cannot be in both train and test.
- 19 junk or ambiguous entries (see ANNOTATION_GUIDE.md).

No sentence appeared under two different labels. Metadata columns were not used: timestamp, consent, fluency, dialect and the free-text feedback question. No record has a missing field. The kit's `validate.py --track intent` passes.

**Group creation and split checks:** `group_id` = contributor + intent (396 groups), so one person's sentences for one intent stay in a single split. Groups were assigned to splits by a seeded hash, aiming for about 70/15/15 with at least 5 dev and 5 test records per label. The final split is 687 / 172 / 165. Every label appears in every split.

**Baseline and final model; dev and frozen-test metrics:** The kit's baseline is character 2–5-gram TF-IDF with logistic regression, unchanged. We did no tuning, and the test set was evaluated once.

| | Accuracy | Macro-F1 |
|---|---|---|
| Dev (172) | 0.901 | 0.897 |
| Test (165) | 0.909 | 0.906 |
| Majority-class baseline (test) | | 0.020 |

Test F1 per label: weather 1.000, datetime 1.000, play_music 1.000, news 0.970, qa_definition 0.938, alarm 0.923, calendar_query 0.867, calendar_set 0.839, lists_createoradd 0.811, lists_query 0.714.

**Analysis of five actual errors** (15 of the 165 test records were wrong; records are referred to by ID only). By type: lists_query read as lists_createoradd 6 times, calendar_query as calendar_set 3, calendar_set as alarm_set 2, and one each of lists_createoradd to alarm_set, lists_query to qa_definition, lists_query to calendar_query, and qa_definition to news_query.

1. `mas-r030-s13-main`: gold lists_query, predicted lists_createoradd. Both list intents share the same long shopping phrase. The short verb that marks reading versus adding is outweighed by the shared character n-grams. The same pattern explains `mas-r010-s13-alt`, `mas-r016-s13-main`, `mas-r016-s14-main`, `mas-r029-s13-main` and `mas-r029-s14-main` (6 of the 15 errors).
2. `mas-r007-s09-main`: gold calendar_query, predicted calendar_set. The sentence uses the verb for "remind me", which appears mostly in calendar_set training sentences. Speakers also use it to ask what is planned. The same applies to `mas-r007-s10-alt` and `mas-r032-s09-main`.
3. `mas-r012-s07-main`: gold calendar_set, predicted alarm_set. The words for "phone" and "time/clock" are strong alarm cues. Without its situation, the sentence is genuinely ambiguous. `mas-r005-s07-main` is similar.
4. `mas-r017-s12-main`: gold lists_createoradd, predicted alarm_set. The sentence is very short, and its "write/set" verb is also used in alarm requests.
5. `mas-r013-s20-alt`: gold qa_definition, predicted news_query. It contains a word that also means "news/report", so the word overlap pulls it towards news.

Overall, the model is excellent where an intent has its own keywords: weather, datetime and play_music all scored 1.0 F1. It confuses intents that share nouns and differ only by a short verb. The English glosses were not checked by a Maa speaker. They are the team's own reading.

**Language variety, limits and unresolved issues:**
- Kaputiei and Kajiado speakers are over-represented.
- Spelling varies.
- The text is written rather than spoken.
- The 4 low-confidence speakers were kept, and the reviewer checked their sentences.
- Next step: collect more lists_query and calendar_query sentences with varied question verbs.
