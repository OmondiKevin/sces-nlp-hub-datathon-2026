# Annotation guide: Team 10 (Kikuyu sentiment, campus cafeteria)

**Task:** label one Kikuyu sentence by the opinion it expresses about the campus cafeteria (food, service, prices, cleanliness, queues, seating).

| Label | Use when | 
|---|---|
| positive | The speaker clearly approves of something | 
| negative | The speaker clearly disapproves or complains |
| neutral | A plain fact or description with no clear opinion |

## Rules
1. Label the opinion, not single words. Negation flips meaning (for example `ti njega` "is not good" is negative even though it contains a positive word).
2. Leave out (and log) sentences that mix opinions, rely on sarcasm, or have an unclear target.
3. One sentence per record. No names, phone numbers or admission numbers.
4. Keep one domain (campus cafeteria) so the data stays consistent.
5. A neutral sentence must contain no praise or complaint, even if it mentions food or prices.

## Process
English source sentences (AI-written, see AI_USE_STATEMENT.md) were given a target label and then translated and adapted into natural Kikuyu by one team member. The label belongs to the sentence's meaning, not to the English words.
