# Quality report

Team: Team 8 (Verity). Language: Kiswahili. Dataset version 1.0, November 2026.

## Accepted contributions

250 records, all with source_method original_human (written by the team): 25 for each of the ten actions. 193 records have at least one slot (77 percent); 57 have none. Slot counts: date 109, item 58, time 50, term 43, location 13, total 273. Location is the smallest class and the results for it should not be over-read.

Unchanged external training rows: none. No external dataset was used and no practice rows are counted.

## Review

Language reviewer: Grace Wangari. Independent review of the 50 test records: [CONFIRM BEFORE SUBMITTING: how many of the 50 Grace checked, and the date. If fewer than 50 were independently reviewed, say so here and in data/contribution.csv, where review_status must match]. Disagreements and resolutions: [ADD ANY, OR WRITE NONE RECORDED].

## Duplicates, exclusions and fixes

Before freezing, the team audited the sheet and corrected the following. Exact and near duplicate sentences were rewritten. Rows whose intent did not match the taxonomy boundary were relabelled or replaced (many general-knowledge questions had been labelled lists_query, and several questions about music had been labelled play_music). Double spaces, a stray character and a real personal name were removed from the text. A slot that was not a date expression was cleared, and span typos were corrected. validate.py passes on the final file (250 records).

Known unresolved choices, which we documented rather than hid: named holidays such as Krismasi and Pasaka are not marked as dates; artist names in play_music are marked as item; music genres in play_music are marked as item; event titles in calendar_set are marked as item, but in two rows the destination place is a separate location slot and only the head word (safari, ziara) is the item.

## Group creation and split checks

Each record has its own group_id unless two records are paraphrases of one situation. validate.py confirms that no group crosses a split and that every split contains every label. The split was built by a script with a fixed seed: 15 train, 5 dev and 5 test per action. All 50 test records are team-written, none rephrased. 37 test records have slots and 13 have none. 24 test records contain a slot value that never appears in the training split; this is the unseen-value subset reported below.

## Models and metrics

Baseline: majority class. Final model: starter character n-gram TF-IDF with logistic regression, plus the training-only slot dictionary. Development metrics are in artifacts/semantic/dev_metrics.json. The test set was evaluated once after the data was frozen.

Frozen test results (50 examples): action accuracy 0.74, macro-F1 0.732; majority baseline accuracy 0.10, macro-F1 0.018. Slot precision 0.741, recall 0.351, F1 0.476. Full-frame exact match 0.32. Unseen-value subset (24 examples): slot F1 0.196, exact match 0.0. Slot F1 on the whole test set is low mainly because recall is low: the dictionary found 20 of 57 gold slots.

## Analysis of five actual errors

The causes below are our hypotheses from reading the predictions and the training vocabulary; we did not run ablations to prove them.

1. sw-112, "Mwezi ujao una likizo ngapi zilizoratibiwa?" (gold calendar_query, predicted datetime_query). The same happened for sw-103 ("Mwezi huu una wikendi ngapi?") and sw-120, and calendar_query recall was only 0.2. Counting and date words such as mwezi, siku and ngapi are common in datetime_query training rows, so the model probably follows the vocabulary. The boundary is also thin in our own data: these questions ask about the calendar but sound like date arithmetic.
2. sw-127, "Ongeza nyanya na vitunguu kwenye orodha ya manunuzi" (gold lists_createoradd, predicted lists_query). The phrase "orodha ya manunuzi" probably appears more in query rows in training, and the action word Ongeza is only a few character n-grams among many. The two item values were unseen, so no slots were found either, and the whole frame failed.
3. sw-147, "Ongeza nyimbo hii kwenye orodha ya nyimbo safarini" (gold lists_createoradd, predicted play_music). The word nyimbo is a strong music cue, which probably outweighs the words Ongeza and orodha.
4. sw-081, "Ongeza ziara ya kuona mwalimu tarehe ishirini Novemba kwa kalenda yangu" (action correct, calendar_set). Both gold slots, the date "tarehe ishirini Novemba" and the event title, were missed because those exact strings were not in the training split. This is the expected unseen-value limit of the memorised dictionary, and it explains why unseen-value exact match is 0.
5. sw-189, "Nipigie muziki wa injili asubuhi hii" (action correct, play_music). The model produced a time slot "asubuhi" where the gold span is "asubuhi hii", so the type is right but the span is wrong and it counts as both a false positive and a miss. The dictionary matches the shorter value it saw in training instead of the full phrase.

## Language variety, limits and unresolved issues

The text is everyday standard Kiswahili written by the team, with Kenyan place names; we did not model dialect or Sheng variation. Some sentences are statements or short commands that a reviewer might label differently. The test set is small, and about half of it is the unseen-value challenge, so the headline slot scores understate performance on common values. The semantic baseline is not an open-ended parser and should not be presented as one.
