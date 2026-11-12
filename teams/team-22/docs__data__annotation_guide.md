# Team 22 Track C annotation guide

## Task

For each single-action Kiswahili request, assign exactly one action label and
annotate every explicit, relevant detail as a slot. Keep the words as written:
do not translate, normalize a local clock expression, infer a date, or execute
the requested action. Exclude unclear, unsupported, or multi-action requests.

## Required action labels

Use these exact Track C labels from the handbook:

| Label | Use when the request asks to… |
| --- | --- |
| `weather_query` | Ask for weather or a forecast. |
| `datetime_query` | Ask for the current time, date, or day. |
| `alarm_set` | Set an alarm that will ring at a requested time. |
| `calendar_set` | Add an event or scheduled reminder to a calendar. |
| `calendar_query` | Read events already on a calendar. |
| `lists_createoradd` | Create a list or add an item to one. |
| `lists_query` | Read an existing list. |
| `play_music` | Start music playback. |
| `news_query` | Read news or headlines. |
| `qa_definition` | Ask for the meaning of a word or concept. |

Use the task-specific contrast in the handbook: for example, a forecast is
`weather_query`, while news about a storm is `news_query`; setting an alarm is
`alarm_set`, while scheduling a calendar event is `calendar_set`.

## Slot types

Only use these five types. A request may have no slots or multiple
non-overlapping slots.

| Type | Include |
| --- | --- |
| `location` | The explicit place or geographic name relevant to the request. |
| `date` | An explicit relative or absolute date/time-period phrase. Preserve its wording. |
| `time` | An explicit clock time or time-of-day phrase. Preserve local clock wording. |
| `item` | The specific event, list entry, media item, or object requested. |
| `term` | The explicit topic, concept, person, or entity the user asks about. |

Capture the smallest complete phrase that expresses the slot, including words
needed to identify a multiword value. Do not include unrelated particles or
punctuation. Do not split a single multiword name or phrase into separate
entities. Never make nested or overlapping slots. Use `[]` when no slot is
present.

## CSV representation and span rules

Store a list in `slots_json`. Each object must have exactly the information
needed for the parse:

```json
[{"type":"location","value":"Nairobi","start":13,"end":20}]
```

- `start` and `end` are zero-based Python Unicode character positions.
- `end` is exclusive; therefore `text[start:end]` must equal `value` exactly.
- Preserve the original script, case, diacritics, and local time expression.
- Include both slot-bearing and slot-free requests in the dataset, and include
  both in test. Mark a test subset whose slot values never appear in training
  and report that subset separately.
- If an annotation is corrected, preserve the original value, reason, reviewer,
  and adjudication evidence in the source log. Mark it
  `corrected_with_evidence`; do not silently overwrite it.

## Review and split procedure

1. The author records the exact request, label, slots, source, and contributor
   code.
2. A competent Kiswahili reviewer checks meaning, naturalness, action label,
   and every character boundary. The reviewer must not be the author of a test
   example.
3. Record disagreements and their resolution. Use pseudonymous codes in the
   public dataset; keep the code-to-person and permission evidence privately.
4. Assign `group_id` by underlying source/example family, not by intent. Keep
   paraphrases of the same source in one split.
5. Use 15 train, 5 validation, and 5 test examples per action at the minimum
   target of 250 accepted records. For Track C, at least 100 records must have
   one or more slots.

## Current dataset

`Team_22_Dataset_Track_C.csv` is the single authoritative dataset and follows
this guide. An independent Kiswahili reviewer approved all 250 rows. Accepted
corrections map `take_note` to `lists_createoradd` and `general_qa` to
`qa_definition`; original labels, accepted labels, reasons, and reviewer codes
are recorded in `../../provenance/track_c_label_correction_log.csv`. The
dataset includes slot-free test coverage and balanced splits. Use
`audit_track_c.py` to check its structure. See the
[quality report](quality_report.md) and
[Track C evidence summary](../model/TRACK_C_EVIDENCE.md).
