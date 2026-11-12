# Groups and splits (issue #6)

**group_id:** contributor code + intent (e.g. `C07-alarm_set`). There are 396 groups. Contributor codes C01–C41 follow the response order in the form. The name-to-code key is private.

**Split assignment:**
- For each intent, the groups are put in a fixed order by the SHA-256 hash of `"13:" + group_id` (seed `13`).
- They are then filled into test until about 15% of that intent's records (at least 5) are in test, then dev until about 15% (at least 5), and the rest go to train.
- A whole group always goes to one split.

**Key rule check:** All of one contributor's answers for an intent stay together, and `validate.py` confirms that no group_id crosses splits. Note: the grouping is by contributor + intent. The same contributor can therefore appear in train for one intent and in test for another. No contributor's answers for the same intent are split across train and test.Splits are made by contributor and intent, so the same contributor can appear in train, dev and test. We did not require each contributor to be entirely in one split, so test scores may be optimistic. 

**Counts:**

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
| **Total** | **687** | **172** | **165** | **1,024** |

Every label meets the 15 / 5 / 5 minimum in every split.
