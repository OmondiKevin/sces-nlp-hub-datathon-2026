# Annotation guide — Team 24 (Kiswahili 5)

Version 1.0, 2026-11-11. Track A, intent classification. 

## Task and exact label set
Each record is **one written request in Kiswahili to a simulated assistant**. The label is the **action the user wants the assistant to take**, not a keyword in the sentence. Ten labels, exactly as in `taxonomy.csv` (MASSIVE-aligned):
`weather_query`, `datetime_query`, `alarm_set`, `calendar_set`, `calendar_query`, `lists_createoradd`, `lists_query`, `play_music`, `news_query`, `qa_definition`.

Quick test for a record: (1) Is it a request to an assistant? (2) What single action would the assistant take? (3) Does that match one label's definition? (4) Does it pass that label's boundary rule? (5) Is it clear, natural and one intent? If any answer is no, exclude it and log why. We do not invent labels to make data fit.

## Primary language and spelling conventions
- Kiswahili, `sw-KE`; everyday Kenyan Swahili in a spoken-request register. Informal forms that are genuinely used are kept (e.g. *Naeza*, *Nikona*, *ama*).
- Standard spelling otherwise (e.g. *asilimia*, *Badilisha*, *redio*, proper nouns capitalised). Spelling corrections made during review are logged (see QUALITY.md).
- The English loanword *alarm* is kept in three rows (24-054, 24-060, 24-071) as genuine code-switching; other alarm rows use *kengele*. We did not add English words to create variety.
- Names, places, genres and teams (e.g. Sauti Sol, Harambee Stars, Zoom, hip hop) are kept as written.
- No personal details (names of private people, phone numbers, emails) are included; examples use common names only.

## Positive examples for each label (all team-authored rows)
| Label | Use when the user wants to… | Example (record) |
|---|---|---|
| `weather_query` | ask for weather or a forecast | *Utabiri wa kesho Nyeri ni upi?* (24-013) |
| `datetime_query` | ask the current time, date or day | *Ni saa ngapi?* (24-028); *Leo ni tarehe ngapi?* (24-027) |
| `alarm_set` | set an alarm that rings at a time | *Weka kengele ya saa mbili usiku.* (24-055) |
| `calendar_set` | add an event or scheduled reminder | *Ongeza mkutano na meneja Ijumaa saa nane kwenye kalenda.* (24-079) |
| `calendar_query` | read existing calendar events | *Nina miadi gani kesho?* (24-106) |
| `lists_createoradd` | create a list or add an item | *Ongeza sukari kwenye orodha ya duka.* (24-132) |
| `lists_query` | read an existing list | *Nisomee orodha ya duka* (24-166) |
| `play_music` | start music playback | *Cheza gengetone.* (24-192) |
| `news_query` | read news or headlines | *Nisomee vichwa vya habari* (24-212) |
| `qa_definition` | ask the meaning of a word or concept | *Usanisinuru ni nini?* (24-239) |

## Boundaries and counterexamples (decisions we applied)
- **Set vs query.** Creating something is `*_set` / `*_createoradd`; reading something that already exists is `*_query`. *Nina miadi gani kesho?* is `calendar_query`; *Weka miadi…* is `calendar_set`. A list question must make clear that a list is meant (we added *orodha* to rows that did not).
- **Reminders** (*Nikumbushe…*, *niwekee ukumbusho…*) are **`calendar_set`** (the handbook's "scheduled reminder"), not `alarm_set`. Rows 24-062, 24-065 and 24-069 were relabelled for this reason.
- **Alarm vs timer.** A request that something rings at a time or after a duration is `alarm_set` (24-056 was reworded to *Weka kengele ipige baada ya dakika kumi.*). Calculating how long you would sleep is not a request to set an alarm (excluded and rewritten).
- **Weather vs news.** A forecast is `weather_query`; asking for news about a storm is `news_query` (handbook rule).
- **Definition vs general question.** `qa_definition` is only "what does this word or concept mean?" (*X ni nini?*, *X ina maana gani?*). Questions about properties, reasons, duties, history or how-to steps are **out of scope**, not `qa_definition`.
- **News vs factual question.** `news_query` asks for news or headlines. A specific factual or history question is out of scope.
- **Out of scope (excluded, not forced into a label):** removing an item from a list, deleting a calendar event, closing a list, stopping music, searching for products or flights, and database-style commands.

## Ambiguous cases to exclude or adjudicate
- Missing context ("these statues"), unclear meaning, or two requests in one sentence: exclude.
- Rows that were close to a label but failed a boundary were **reworded** by the team (same situation, supported action) and re-reviewed, with the old and new text logged. Examples: 24-142, 24-157, 24-209, 24-105, 24-077 (originally removal/closing/stopping/calculation requests).
- An initial batch of 110 rows from an external repository was excluded entirely (licence/provenance, and most did not fit any label). See DATA_CARD.md.

## Independent review and disagreement resolution
- Every test row was checked by a person other than its recorded author (43 by Moses/24M, 9 by Nathan/24N).
- Concerns were raised before the test review (7 test rows with label or wording doubts). The team reworded them; because Moses had approved that wording, Nathan reviewed those rows he did not write; rows 24-209 and 24-235 (written by Nathan) were reviewed by Moses. No other reviewer disagreements were recorded.
- Resolution rule: if the reviewer and author disagree on a label, the row is reworded to a clear single intent or excluded; it is never kept with a forced label. 

## Version and date
- v1.0, 2026-11-11 (written at submission time from the working logs; its rules summarise the handbook definitions and the review decisions above, rather than being a document used before annotation).
