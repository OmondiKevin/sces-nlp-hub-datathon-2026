# Kinyarwanda sentiment annotation guide

**Project:** Team 16, sentence-level sentiment analysis  
**Labels:** `positive`, `negative`, `neutral`  
**Working revision:** 1.3, 10 November 2026

## Task and labels

Assign one label to the sentiment expressed in the sentence. Judge the writer's expressed evaluation, not whether the topic is usually good or bad.

- **Positive:** clear approval, satisfaction, gratitude, praise, enjoyment, or a favorable outcome expressed positively.
- **Negative:** clear complaint, disappointment, harm, failure, dissatisfaction, or an unfavorable outcome.
- **Neutral:** factual or informational wording without a clear positive or negative evaluation. A mildly favorable fact is still neutral when the writer does not express approval or emotion.

## Language and writing conventions

- Use natural Kinyarwanda spelling, agreement, punctuation, and apostrophes. Preserve the intended Kinyarwanda wording; do not translate literally from English when that produces an awkward phrase.
- Include a mix of everyday and written registers. Avoid making every example sound like a report, press release, or official announcement; do not force slang.
- Keep each record to one coherent sentence or short utterance. Do not include identifying personal information.
- Normalize text to Unicode NFC before checking for duplicates. Keep spelling and punctuation in the source text unless an annotator is correcting a documented error.

## Anchor examples

| Label | Example | Note |
|---|---|---|
| Positive | `Twafatanyije neza kandi twese byaradushimishije.` | Positive cooperation and shared happiness; wording revised after native-speaker feedback. |
| Negative | `Ibyo badusezeranyije byose byabaye imfabusa ku munota wa nyuma.` | The reviewer judged this negative and considered `byabaye imfabusa` idiomatic. The phrase `ku munota wa nyuma` may be an English calque and remains a wording question. |
| Neutral | `Byose byagenze nk’uko byari biteganyijwe.` | A factual status statement; mildly favorable implication alone does not make it positive. |
| Neutral | `Inyandiko yacu igizwe n’ibice bitandatu byose hamwe.` | Descriptive statement with no expressed evaluation. |
| Neutral | `Igiciro cy’ibiribwa cyagumye ku rugero rumwe muri uku kwezi.` | Factual report; price stability is not explicitly praised or criticized. |

## Boundaries and adjudication

- For mixed or contrastive wording, use the dominant expressed sentiment only when it is clear. If neither polarity dominates, send it for adjudication or exclude it; do not force a label.
- Do not infer sentiment from topic alone. A sentence about prices, a schedule, or a completed task can be neutral even if a reader might personally welcome the fact.
- Treat idioms, sarcasm, and culturally dependent expressions cautiously. Ask a fluent reviewer when intent or naturalness is uncertain.
- If a sentence is understandable but may be an English calque, record that concern and seek a native-speaker rewrite before treating it as a language-quality anchor.

## Review and disagreements

The project plan names Innocent Mukiza (`reviewer_001`) as the native Kinyarwanda reviewer. Reviewers should work independently from the contributor, record the proposed label and any wording correction, then resolve disagreements with a short rationale. Keep the original wording and the decision trace when a human changes a label or text. Every test item must have documented independent review.

The five examples in the 10 November 2026 feedback were adjudicated as follows: `kin-015` neutral, `kin-155` negative, `kin-314` positive with a wording revision, and `kin-319` and `kin-327` neutral. The reviewer's note on `kin-155`'s `ku munota wa nyuma` wording remains unresolved.

