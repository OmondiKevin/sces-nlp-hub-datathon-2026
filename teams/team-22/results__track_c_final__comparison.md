# Track C final test results

The final model and every baseline were evaluated on the same frozen test split of 50 examples, five per action. The final run used `castorini/afriberta_large`, seed 42, and epoch 8 selected on validation data.

| System | Intent accuracy | Intent macro-F1 | Exact slot precision | Exact slot recall | Exact slot F1 | Full-frame exact match | JSON validity | Unseen-value exact recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AfriBERTa joint model | 1.0000 | 1.0000 | 0.8533 | 0.7356 | 0.7901 | 0.5800 | 1.0000 | 0.5833 |
| Majority intent | 0.1000 | 0.0182 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 |
| Character TF-IDF intent | 0.8600 | 0.8565 | 0.0000 | 0.0000 | 0.0000 | 0.0400 | 1.0000 | 0.0000 |
| Character TF-IDF + train-only surface matcher | 0.8600 | 0.8565 | 0.7647 | 0.4483 | 0.5652 | 0.2400 | 1.0000 | 0.0000 |

Slot scoring requires the exact type and Unicode character boundaries. Full-frame exact match requires the correct intent and complete slot set. Unseen-value exact recall measures recovery of test `(type, value)` pairs absent from training. The model's test JSON was valid for all 50 examples.

The final model made five full-frame errors: it missed the item `shughuli` in `rec_028`; missed `sherehe ya kuzaliwa` in `rec_055`; added a false location `Kiswahili` in `rec_083`; returned only `afya` for `afya bora` in `rec_106`; and missed `mechi yao ya kirafiki` in `rec_153`. Per-label metrics and detailed error records are in [`metrics_and_errors.json`](../../models/track_c_final/metrics_and_errors.json); full baseline outputs are in [`../track_c_baselines/`](../track_c_baselines/). Metric definitions and test-split history are in [`MODEL_EVALUATION_PROTOCOL.md`](../../docs/model/MODEL_EVALUATION_PROTOCOL.md).

The final training CSV SHA-256 was `0756d1b54581bd23eab36a0455e987e3ca6d45d51f61ab5f544d146058509193`. The submitted CSV SHA-256 is `0e10c800925e101af08aee1213f55543dcc508a024da918d6c87d3a96703835f`; only permission-reference and adjudication-note metadata changed, leaving model inputs unchanged.
