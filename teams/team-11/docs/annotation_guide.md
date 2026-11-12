# Dholuo Sentiment Annotation Guide

**Team:** Team 11  
**Language:** Dholuo  
**Task:** Sentiment Classification  
**Status:** Draft – requires team review and linguistic validation  
**Version:** 1.0

## 1. Purpose

This guide defines the annotation rules used to classify Dholuo text into three sentiment categories: positive, negative and neutral.

The purpose is to promote consistent, evidence-based labels and reduce disagreements between contributors and reviewers.

## 2. Sentiment categories

| Label | Definition | Annotation guidance |
|---|---|---|
| Positive | The text expresses satisfaction, approval, happiness, gratitude, encouragement or another favourable opinion. | Assign when the overall expressed sentiment is favourable. |
| Negative | The text expresses dissatisfaction, disappointment, anger, criticism, sadness or another unfavourable opinion. | Assign when the overall expressed sentiment is unfavourable. |
| Neutral | The text communicates information, asks a question or makes a statement without a clearly expressed positive or negative sentiment. | Assign when there is insufficient evidence of either positive or negative sentiment. |

## 3. Annotation rules

1. **Read the entire sentence.** Do not assign a label based on one word without considering the surrounding meaning.
2. **Prioritise expressed meaning.** Classify the sentiment conveyed by the text, not what the annotator assumes the speaker feels.
3. **Do not confuse events with sentiment.** A sentence describing an event is not automatically positive or negative.
4. **Use neutral carefully.** Neutral does not mean that the sentence is difficult to understand. It means that no clear positive or negative sentiment is expressed.
5. **Consider context.** Where context is necessary to interpret a sentence, record the uncertainty rather than inventing missing information.
6. **Do not automatically treat questions as neutral.** A question may express frustration, criticism or excitement.
7. **Watch for negation.** Words that reverse or modify meaning must be considered in the context of the complete sentence.
8. **Do not assume sarcasm.** Only assign an implied sentiment where the meaning is sufficiently clear and supported.
9. **Preserve the original text.** Do not silently rewrite sentences to make them fit a particular label.
10. **Flag uncertain language.** Sentences with unclear wording, dialect differences or possible translation errors should be escalated for linguistic review.

## 4. Handling difficult cases

| Situation | Recommended approach |
|---|---|
| Mixed positive and negative opinions | Consider the dominant expressed sentiment. If it cannot be determined reliably, flag for review. |
| Negation | Interpret the complete phrase rather than individual sentiment words. |
| Sarcasm or irony | Flag for review unless the intended sentiment is clear to a proficient speaker. |
| Questions | Determine whether the wording itself expresses sentiment. |
| Factual statements | Usually neutral when no opinion or emotional evaluation is expressed. |
| Unclear or unnatural Dholuo | Flag for linguistic review; do not guess the intended meaning. |
| Code-switching | Assess whether the sentence remains understandable and whether the sentiment can be reliably established. |

## 5. Independent review procedure

Independent review should be conducted by someone other than the original contributor of the record.

The reviewer should:

1. Read the Dholuo sentence without first seeing the original sentiment label.
2. Assign an independent label: positive, negative or neutral.
3. Record comments where the meaning or sentiment is uncertain.
4. Compare the independent label with the original label.
5. Record whether the original label is accepted, corrected or disputed.
6. Escalate disagreements for discussion with a proficient Dholuo speaker.

The review record should retain the original label, reviewer label, final decision, reviewer code and review date.

Independent review must only be recorded as completed when the procedure has actually taken place.

## 6. Quality assurance

Before a record is accepted into the final contribution dataset, check that:

- The text is genuinely Dholuo and linguistically understandable.
- The sentence is distinct from other records after normalisation.
- The sentiment label is supported by the sentence's meaning.
- The record has a unique identifier.
- The contributor and source metadata are accurate.
- The train, development or test split is retained as intended.
- Any uncertainty or correction is documented.

## 7. Limitations

Sentiment interpretation may vary with dialect, context, idioms, sarcasm and cultural expressions. Machine-translated sentences may also contain unnatural wording or contextual errors.

This guide does not claim to resolve all linguistic ambiguities. Records that cannot be reliably interpreted should be flagged rather than assigned an unsupported label.

## 8. Team approval

This guide should be reviewed and approved by the team's contributors and a Dholuo-proficient reviewer before being treated as the final annotation policy.

**Approval status:** Pending team and linguistic review.