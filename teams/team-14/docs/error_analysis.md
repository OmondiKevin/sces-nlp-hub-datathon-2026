# Error Analysis

This document analyses 5 real prediction errors from `artifacts/intent/test_predictions.csv` for the Maa intent tracking task.

## Error 1
- **Record ID:** `mas-r005-s07-main`
- **True Label:** `calendar_set`
- **Predicted Label:** `alarm_set`
- **Text:** "Siraka enkumoi te simu emouto nchere mmeolku."
- **Likely Cause:** Semantic overlap between setting a calendar event reminder/notification and setting an alarm on a mobile device, as both involve time-based phone configurations and similar phrasing regarding phone alerts (`simu`).

## Error 2
- **Record ID:** `mas-r012-s07-main`
- **True Label:** `calendar_set`
- **Predicted Label:** `alarm_set`
- **Text:** "Kayiu napik e simu esaa"
- **Likely Cause:** Lexical confusion involving timepieces or clock settings (`esaa` / time) on a mobile phone (`simu`), leading the model to incorrectly classify a calendar scheduling request as an alarm configuration.

## Error 3
- **Record ID:** `mas-r007-s09-main`
- **True Label:** `calendar_query`
- **Predicted Label:** `calendar_set`
- **Test Text:** "Ntadamuaki nkolati eduo taata"
- **Likely Cause:** Ambiguity in query verbs dealing with appointments or schedules for today (`taata`). The model confused looking up or checking a calendar entry (`calendar_query`) with creating or scheduling a new entry (`calendar_set`).

## Error 4
- **Record ID:** `mas-r007-s10-alt`
- **True Label:** `calendar_query`
- **Predicted Label:** `calendar_set`
- **Test Text:** "Ntadamuaki enkolat entariki naje"
- **Likely Cause:** Similar vocabulary structures between retrieving schedule details and setting diary entries. The keyword related to dates/appointments triggered a modification intent instead of a retrieval intent.

## Error 5
- **Record ID:** `mas-r032-s09-main`
- **True Label:** `calendar_query`
- **Predicted Label:** `calendar_set`
- **Test Text:** "Ntadamwagi entumo etaata"
- **Likely Cause:** Over-reliance on action-oriented lexical tokens in the prompt referring to meetings/events (`entumo`) for today (`taata`), causing the classifier to mistake a read/query operation for a write/set operation.