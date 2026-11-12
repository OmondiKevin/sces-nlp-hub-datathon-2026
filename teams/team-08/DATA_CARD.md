# Dataset card and source log

Team 8 (Verity). Primary language: Kiswahili (standard, Kenyan usage). Version 1.0, November 2026.

## Task and intended use

Limited semantic parsing: classify a short request into one of ten actions and extract surface slots (location, date, time, item, term). Intended for a small prototype that shows the recognised action and slots. Not for open-ended understanding, real actions, date conversion, or any use that needs a reliable general parser.

## Fields, counts and splits

Fields follow the starter kit semantic template: record_id, language, text, label, source_dataset, source_version, source_record_id, source_url, source_method, licence_or_permission, contributor_code, reviewer_code, review_status, group_id, split, slots_json.
250 records: 25 per action. Split 150 train, 50 dev, 50 test (15, 5, 5 per action). 193 records have slots; 57 have none. Slot counts: date 109, item 58, time 50, term 43, location 13. slots_json is a JSON list of {type, value, start, end} with Python Unicode character offsets, start inclusive and end exclusive.

## Sources

All text is original, written by the team (source_method original_human). source_dataset: strathmore_team_original, version 1.0, source_url not_applicable, source_record_id is the row number in the annotation spreadsheet. No external dataset, translation or downloaded text is included. Transformations: spreadsheet slots converted to JSON with offsets computed by data/make_contribution.py.

## Contributor permission

The sentences were written by team members for this datathon, with no real names, phone numbers or private content intended. [CONFIRM: each writer agrees to release under CC0. Private permission evidence is held separately and is not in the repository.] licence_or_permission is CC0.

## Annotation and review

Slots were first drafted and then reviewed by the team (see CONTRIBUTIONS.md). Grace Wangari reviewed the language [CONFIRM SCOPE AND TEST-ROW COUNT]. Rules are in ANNOTATION_GUIDE.md.

## Known limitations and excluded uses

Small size; one language variety; label boundaries between calendar_query and datetime_query and between lists_query and lists_createoradd are close; item and term rules are team conventions; location has only 13 slots; named holidays are not marked as dates. Do not use it to evaluate general Kiswahili understanding, to infer personal information, or as a benchmark for other tasks.

## Credit and correction

Contact through the organiser-approved channel. Starter code and taxonomy: Strathmore NLP Hub Datathon starter kit v2.

## Release terms

Proposed release under CC0 for the data. Pending decision: confirmation from all contributors, and any restrictions the organisers apply.
