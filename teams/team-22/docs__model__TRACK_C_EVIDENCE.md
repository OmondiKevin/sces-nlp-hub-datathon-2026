# Team 22 Track C evidence

Team 22's submission uses **Track C: limited semantic parsing** for Kiswahili.
The solution predicts one handbook action and extracts exact character spans
for `location`, `date`, `time`, `item`, and `term`.

| Judging area | Evidence |
| --- | --- |
| Data quality and annotation | The sole contribution CSV has 250 unique requests, 25 per action, and 15/5/5 train/validation/test splits. All rows are marked independently reviewed. The 50 accepted label corrections are logged. The structural audit finds 475 valid slot annotations, both slot-bearing and slot-free test examples, and no span/schema issues. |
| Provenance, ethics, and rights | The row-level source log records source/version, collection method, pseudonymous contributor and reviewer codes, split, and correction details. The request text is team-authored. Permission covers this Datathon submission and assessment; no open-data license is claimed. Private permission evidence and identity keys are not included in the public submission package. |
| Contribution coverage and balance | Each of the ten actions has 25 requests. The dataset contains 239 slot-bearing rows, all five allowed slot types, and 338 exact slot type/value pairs. The test set includes 51 slot values not present in training. |
| Baselines and evaluation | The AfriBERTa joint model was compared on the same frozen 50-row test set with majority intent, character TF-IDF, an empty-slot comparator, and a train-only surface-value matcher. The final model scored 100.00% intent accuracy and macro-F1, 79.01% exact-span slot F1, 58.00% full-frame exact match, 100.00% JSON validity, and 58.33% unseen-value exact recall. |
| Reproducibility and documentation | Training, validation selection, final evaluation, artifact backup, and demo commands are documented in the Colab run guide. The final checkpoint is not included in Git. Training CSV SHA-256: `0756d1b54581bd23eab36a0455e987e3ca6d45d51f61ab5f544d146058509193`; submitted CSV SHA-256 after metadata-only privacy and wording updates: `0e10c800925e101af08aee1213f55543dcc508a024da918d6c87d3a96703835f`. Checkpoint SHA-256: `25939b8a36c84453414a069e0e92fdb92437d347823ae0767ad618305f1fd971`. |
| Demonstration, explanation, and teamwork | Sauti provides a browser interface with a Kiswahili explanation, inspectable JSON frame, and clarification choices for selected low-confidence calendar predictions. The interface simulates parses and does not execute actions. Member roles and AI assistance are recorded in the contribution statement. |

The test set contains five examples per action and was selected from the former
training split after the former test had been used during model development.
It is a fresh split, not a prospective sample. The model's full-frame exact
match and unseen-value recall leave substantial room for improvement. The
evaluation protocol reports actual errors and defines every metric.

## Evidence files

- [Dataset and quality report](../data/quality_report.md)
- [Dataset card and annotation guide](../data/dataset_card.md)
- [Source log, correction log, and split record](../../provenance/)
- [Model protocol, baseline comparison, and test errors](MODEL_EVALUATION_PROTOCOL.md)
- [Colab reproduction and Sauti run guide](COLAB_TRACK_C_RUN.md)
- [Contribution and AI-use statement](../team/contribution_and_ai_use.md)
