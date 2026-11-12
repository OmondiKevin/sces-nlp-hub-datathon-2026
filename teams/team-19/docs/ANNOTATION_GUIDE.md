# Annotation guide (Team 19, Kiswahili, v1.0, 12 Nov 2026)

**Task and label set:** one intent per sentence from the 10 labels in `taxonomy.csv`: weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query, qa_definition.

**Language and spelling:** Kenyan Kiswahili (`sw-KE`). Natural Sheng and Kiswahili–English code-switching are kept ("Nipee time", "Seti alarm"). Informal spellings that speakers really use are kept; keyboard typos and paste artefacts are corrected.

**Positive examples (from the data):**
- weather_query: "inaeza nyesha leo kweli?", "ni degree ngapi nje?"
- datetime_query: "Tafadhali niambie tarehe.", "kesho ni tarehe gani?"
- alarm_set: "Niamshe saa kumi", "weka alarm ya mapema"
- calendar_set: "Weka makumbusho ya tarehe 24 Novemba naenda graduation"
- calendar_query: "Nina mikutano gani kwenye kalenda yangu leo?", "Exam ni lini?"
- play_music: "niwekee wimbo aina ya bongo", "weka nyimbo za gospel"
- news_query: "nipatie habari za michezo", "nipee habari za eneo la Nairobi"

**Boundaries and counterexamples:**
- Asking a date or day → datetime_query, even if it mentions an event day. Asking *when an event is* or *what is planned* → calendar_query. *Adding* an event → calendar_set.
- alarm_set is only setting a new alarm; snooze, turn off, volume, ringtone and complaints are out of scope.
- play_music is only a request to play; volume, stop, skip, download and add-to-playlist are out of scope.
- news_query is a request for news; comments about the news are out of scope. Weather forecasts are weather_query.

**Out of scope (rewritten during review):** comments, complaints, fragments with no request, and requests outside the 10 labels (timers, volume, snooze, ringtone, stop/skip). Logged in `data/review_changes.csv`.

**Review and disagreements:** every test record is reviewed by a Kiswahili speaker who did not write it; disagreements are resolved by discussion and logged in `docs/QUALITY.md`.
