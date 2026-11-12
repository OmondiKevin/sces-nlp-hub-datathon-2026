# Annotation guide

**Task and exact label set:** Each sentence gets one intent from: weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query, qa_definition.

**Primary language and spelling conventions:** Maa (`mas`). Contributors' own spelling is kept. We only normalised:
- Unicode (NFC) and spaces.
- One apostrophe character for the velar nasal *ng'* (’ ‘ ^ " were all changed to ').
- Repeated punctuation ("??" became "?") and "......" placeholders were removed.
- English notes typed inside answers, such as "(name of the song)", were removed.
- Code-mixed Swahili or English words that speakers really use, such as *alarm*, *kalenda* and *biashara*, were kept.

**Positive examples for each label** (the form situation that produced it):

| Label | Situations in the form | Example |
|---|---|---|
| weather_query | will it rain later; will it be hot tomorrow | *Kesha sa taata?* / *Keirowua taisere?* |
| datetime_query | what time is it; what is today's date | *Kesaaja tenakata?* / *Kanu duo taata?* |
| alarm_set | wake me for an early journey; ring this afternoon | *Inyoyieki saa tomon enkakenya* |
| calendar_set | put a meeting in the calendar; save a family event | *Ntadamuaki entumo e jumamosi* |
| calendar_query | what is planned today; am I free on a day | *Kakua tumoritin aata taata?* |
| lists_createoradd | start a shopping list; add one item | *Ntobirakaki empalai enkinyianga* / *Toponai ena* |
| lists_query | read my shopping list; show my to-do list | *Isumakaki nena tokitin nainyanguni* |
| play_music | play music now; play a certain song or singer | *Taranya osinkolio* |
| news_query | today's headlines; news on sport or the economy | *Isumakaki ilomon le taata* |
| qa_definition | what does a word mean; explain an idea | *Kainyoo eji ele rorei?* |

**Boundaries and counterexamples:**
- Asking *what is on* a list belongs to lists_query, even when it was written in a "make a list" situation.
- Asking *what is planned* is calendar_query. Asking to *save or remind me of* an event is calendar_set.
- Single verbs that fit several intents, such as *Sumakaki* ("read to me", which works for lists and news), were excluded.

**Ambiguous cases to exclude or adjudicate:** We removed 19 sentences:
- 4 answers that were not Maa ("No", "not sure").
- 8 single words that could mean more than one intent.
- 5 noun phrases with no request in them (e.g. *Entumo olmarei*, "family meeting").
- 2 sentences in the "make a list" situations that actually ask what to buy.

Each removed sentence and the reason is logged in `data/raw/dropped_rows.csv` (private).

**Independent review and disagreement resolution:** All 1,024 records were reviewed by a Maa speaker who did not write them (reviewer code R01). The reviewer deleted 136 of the 1,247 raw answers (105 non-answers such as "No" or "N A", and 31 that did not fit the situation) and corrected the spelling of 124. See QUALITY.md. After that, the automatic cleaning removed 68 duplicates and 19 ambiguous sentences.

**Version/date and changes:** v2026-11, 11 November 2026. First release.
