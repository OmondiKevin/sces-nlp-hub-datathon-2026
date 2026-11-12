# Annotation guide — pending language reviewer approval
Label the requested action, not a shared keyword. Use exactly the ten labels in taxonomy.csv. Its English/Kiswahili examples explain boundaries; they are not Kikuyu contributions.

| Label | Include | Boundary |
|---|---|---|
| weather_query | Request a forecast/current weather | News about a storm is news_query |
| datetime_query | Ask the current date/time/day | Request an alarm is alarm_set |
| alarm_set | Make an alarm ring | Schedule an event is calendar_set |
| calendar_set | Add an event/scheduled reminder | Read events is calendar_query |
| calendar_query | Read existing calendar events | Creating events is calendar_set |
| lists_createoradd | Create a list/add an item | Read contents is lists_query |
| lists_query | Read an existing list | Adding items is lists_createoradd |
| play_music | Start music playback | Artist facts are outside this label |
| news_query | Request news/headlines | Forecast is weather_query |
| qa_definition | Ask meaning of a word/concept | General factual QA is outside scope |

Write natural Kikuyu from real imagined use situations. Vary wording, context, politeness, length and syntax; avoid bulk slot substitution. Do not translate a single template 25 times. Preserve meaningful diacritics; agree spelling and variety with a competent reviewer. Record genuine code-switching and dialect choices. No generated text is presented as human-authored.
Exclude unsupported, ambiguous or multiple-intent utterances; record the reason rather than forcing a label. Resolve language or label disagreements with competent review, keeping before/after evidence. Do not silently replace difficult test examples after seeing model errors.
Review each accepted record for naturalness, clear single intent, correct label, privacy, source terms and duplicate families. Log exact final text/label and decision. Independently review all test records; review a sample of other records independently too. A corrected text or label requires a new matching accepted review entry.
Collection suggestions (English situations, not dataset sentences): tomorrow's rain, today's day, a morning wake-up alarm, scheduling a study meeting, checking tomorrow's events, adding food to a shopping list, reading that list, playing a song, current headlines, and asking what a concept means. Authors formulate their own natural Kikuyu expressions.
