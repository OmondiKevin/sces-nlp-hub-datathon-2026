# Annotation guide
* **Task and exact label set:** Track A (Intent Classification). 10 MASSIVE-aligned labels: `weather_query`, `datetime_query`, `alarm_set`, `calendar_set`, `calendar_query`, `lists_createoradd`, `lists_query`, `play_music`, `news_query`, `qa_definition`.
* **Primary language and spelling conventions:** Kiswahili (sw-KE), specifically conversational Kenyan Swahili. Natural code-switching (e.g., using "diary", "meeting", "clients") and local phrasing (e.g., "shags", "ndinga", "bash") are preserved to reflect authentic daily usage. Punctuation (like commas) is omitted to simplify parsing.
* **Positive examples for each label:**
  * `calendar_set`: "Naomba uniwekee mkutano wa ofisi Jumatatu saa nne asubuhi"
  * `weather_query`: "Je kutakuwa na mvua kesho?"
  * `lists_createoradd`: "Maziwa na sukari zimeisha tafadhali ziweke kwenye orodha."
* **Boundaries and counterexamples:** 
  * *Boundary:* "Weka ukumbusho wa daktari kesho jioni saa kumi" is `calendar_set` (event scheduling) rather than `alarm_set` (waking up or a simple timer).
  * *Boundary:* "Nisomee orodha ya majukumu ya leo asubuhi" is `lists_query` (reading a list), not `calendar_query` (reading an itinerary).
* **Ambiguous cases to exclude or adjudicate:** Multi-intent sentences such as "Soma vichwa vya habari kisha uweke kengele ya saa mbili" (News + Alarm) are excluded from this dataset to ensure single-label clarity.
* **Semantic only: permitted slot types and offset convention:** Not applicable (Track A).
* **Independent review and disagreement resolution:** All `test` records are independently reviewed using a round-robin system (e.g., T04-B authors, T04-Z reviews). Disagreements on phrasing naturalness or label boundaries are discussed via team consensus before inclusion.
* **Version/date and changes:** v1.0, 10 November 2026.[cite: 53, 58]