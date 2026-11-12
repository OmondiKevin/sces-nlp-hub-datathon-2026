# Annotation guide

Version 1.0, November 2026. Language: Kiswahili.

## Task and labels

Each request gets one action label, chosen by what the person wants done, not how they feel. The ten labels are weather_query (ask about weather), datetime_query (ask the current date or time, or a date fact), alarm_set (set an alarm or wake-up reminder), calendar_set (create a calendar event), calendar_query (ask about or check existing events), lists_createoradd (create a list or add items), lists_query (read or check the user's own list), play_music (request playback), news_query (ask for news) and qa_definition (ask the meaning of a word or concept).

## Language and spelling

Everyday standard Kiswahili as a person would type to an assistant. Typos are corrected before freezing so slot spans match the text. No real names, numbers or private content.

## Boundaries and counterexamples

A storm in the news is news_query, a forecast is weather_query. Setting an alarm is alarm_set, scheduling a meeting is calendar_set; reminders that ring at a time are written as alarm requests (Weka kengele ya kunikumbusha). Creating an event is calendar_set, asking or confirming what is on the calendar is calendar_query. Adding an item to a list is lists_createoradd, reading or checking a list is lists_query. General-knowledge questions that do not refer to the user's own list are not lists_query. Questions about a song, album or genre are not play_music; only requests to play are. Other factual questions that are not asking for a meaning are out of scope.

## Slot types and rules

Types: location, date, time, item, term. Copy the words exactly as in the text, with no punctuation, and mark the shortest natural phrase.
Location: a place (Nairobi, Mombasa, Afrika Mashariki).
Date: a day expression kept as text (kesho, leo, Jumatatu, wiki ijayo, mwezi huu, mwaka huu, jana). A written date is one span including tarehe ("tarehe nane Januari").
Time: a clock time or time of day (saa tatu asubuhi, jioni, sasa hivi, mchana huu). A full phrase such as "saa tatu asubuhi" is one span. "kesho saa tatu" is two slots, a date and a time.
Item: the thing acted on: a list item, a calendar event title, a song, artist or music genre.
Term: a word or topic being looked up or reported on: the defined word, or the news topic.
Do not mark pointers that need earlier context (huko, hapo, hiyo, huu), names of private people, or named holidays (Krismasi, Pasaka). Where an event title contains a place that is also marked as a location, only the head word of the title is the item. Slots may not overlap. Leave the slot cell empty if no slot fits.
Offsets are never typed by hand; a script computes them as Python Unicode character indices, start inclusive, end exclusive, and checks text[start:end] equals the value.

## Ambiguous cases

Unsure cases were left unmarked and logged in the Borderline log tab of the spreadsheet. Examples: lowercase "utawala" (a possible place name), seasons such as masika, Christmas and Easter, the place Toi inside an event title, and artist names against the rule on names of people. These were settled by the team and reviewer or left unmarked.

## Independent review and disagreements

A reviewer other than the writer checks the language, the label and the slots, and every test record needs independent review [CONFIRM STATUS]. Disagreements are discussed and the sentence is corrected or replaced; a record that cannot be agreed is excluded and logged.

## Changes

1.0: first release, November 2026. Changes before freezing: duplicate and near-duplicate rewrites, relabelled or replaced rows that broke the boundaries above, slot span fixes, event titles added as item slots in calendar_set.
