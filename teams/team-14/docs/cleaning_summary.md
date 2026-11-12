# Cleaning summary (issue #5)

Counts only. No Maa text, names or row contents are included. The responses file and every intermediate file are kept outside the repository.

**Input:** The Google Form "How would you say it in Maa" export. It has 42 rows: 41 real responses, plus one stray row holding label names, which was removed. There are 20 situations (2 per intent), each with a main answer and an optional "another way" answer, giving 40 answer columns.

**Method:** This was not Philip's `build_candidates.py`. The team used its own process, in two stages.

**Stage 1: independent Maa reviewer (R01), editing the form export directly**

| Step | Answers |
|---|---|
| Non-empty answers in the raw export | 1,247 |
| Deleted as placeholder or non-answer ("No", "Yes", "N/A", "pass", "Not sure", ...) | 105 |
| Deleted as not fitting the situation (wrong topic, a bare word, half English, a `____` placeholder) | 31 |
| Corrected (spelling, word breaks, emoji or English notes removed, autocorrect damage fixed) | 124 |
| Remaining after review | 1,111 |

**Stage 2: a scripted clean of the reviewed export** (`clean_responses.py`, written with AI help and kept outside the repository)

| Step | Answers |
|---|---|
| Responses without consent | 0 (all 41 agreed) |
| Metadata columns dropped: timestamp, consent, fluency, dialect, feedback | (columns, not rows) |
| Text normalised: Unicode NFC, spacing, one apostrophe for ng', repeated punctuation, "......" placeholders, English notes in brackets | 0 removed |
| Duplicates (same text after ignoring case, punctuation and spacing) | 68 |
| Hand-excluded as non-Maa ("No", "not sure") | 4 |
| Hand-excluded single words that could fit several intents | 8 |
| Hand-excluded noun phrases with no request | 5 |
| Hand-excluded sentences in a "make a list" situation that actually ask what is on the list | 2 |
| Same text under two different labels | 0 |
| **Final records in `data/contribution.csv`** | **1,024** |

**Fluency:** No contributor was dropped for fluency. 29 said Maa is their first language or they speak it fluently, 8 that they use it comfortably every day, and 4 that they know some Maa but are not confident. The 4 low-confidence contributors' answers were kept, because the independent reviewer checked every answer. The form asked for fluent speakers, but its screening did not exclude these respondents. Team decision: kept, because R01 checked every answer. Listed as a limitation.

The per-row exclusion log (`dropped_rows.csv`) contains Maa text, so it is held privately and not committed.
