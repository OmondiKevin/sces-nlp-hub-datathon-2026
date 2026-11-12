# Quality and actual error analysis

Validation passed for330 records and all required metadata. Ten labels have23/5/5 train/dev/test. Normalised exact duplicates:0. The35 lexical-related pairs belong to connected groups that do not cross splits. No prediction was used for test selection. The frozen model and data hashes are in artifacts/intent/freeze_record.json.

The final model scored40/50, accuracy0.80, macro-F1 0.7972261072261072. Original250 model on the same fresh test:36/50, accuracy0.72, macro-F1 0.7148573648573648. There are10 final errors. No settings or labels were changed in response. Historical98% refers to a different old test.

## Five observed errors

| Record | Supplied text | Expected | Predicted |
|---|---|---|---|
| T13-02-29 | Ndagũthaitha, njĩĩre thaa. | datetime_query | alarm_set |
| T13-02-32 | Thaa thaici? | datetime_query | alarm_set |
| T13-03-29 | Ĩkĩra alamu thaa mũgwanja mũthenya o mũthenya wa thikũ ciothe cia wĩra. | alarm_set | datetime_query |
| T13-05-28 | Kwĩna kĩndũ bataire kwĩhaarĩria Njumaa na Kiumia? | calendar_query | weather_query |
| T13-05-33 | Hihi nĩndi na ihinda rĩa guikara muthenya Wa gatano thutha wa mũthenya? | calendar_query | datetime_query |

The first three examples show date/time and alarm confusions. Shared time vocabulary is a plausible hypothesis, not a demonstrated causal diagnosis. The calendar examples were routed to weather/time; fluent review of context and training coverage could help future work. All10 errors can be inspected in test_predictions.csv; the five above are actual errors, not invented examples. No extra review outcome or correction is claimed.

Limits: tiny balanced test with5 records per label; new test allfrom one author; lexical grouping may miss semantic paraphrases; spelling/dialect coverage unquantified; team-confirmed language review is not an independent audit. Probabilities are uncalibrated and out-of-scope text is forced into one of ten classes. Browser/Python parity passed334 cases, identical labels, maximum probability difference1.11e-15; this checks implementation equivalence, not linguistic accuracy. Future work: author-diverse heldout data, genuine semantic-duplicate review and out-of-scope detection, evaluated with new data rather than tuning on this test.
