# Team 13 | Kikuyu 2 | Track A

A text request router for Kikuyu: ten fixed intents, a small reviewed dataset, a reproducible baseline and a public browser demo. It recognises intent and displays a simulated next step; it does not call external action services.

- **Team:** Nadine Njora; Wanyingi Shirleen Muthoni; Celestine Nyingi.
- **Original source repository:** https://github.com/NadineNjora/team13-kikuyu-intent-classification
- **Frozen full source commit SHA:** recorded in the central submission README and submission manifest; the central PR is the submission receipt.

- **Demo** Video
Watch our  presentation and live demo here: https://www.loom.com/share/7c5163a6c03c4132ab08cbc60355914d

- **User-edited Colab:** https://colab.research.google.com/drive/1AammOdAro-P--_l1mp5X94m8nnnKdxHw?usp=sharing

## Data and independent review

`data/contribution.csv` contains **330 accepted records, 33 per intent**. Batches: 100 A1/R1; 100 A2/R2; 50 A3/R3; 80 A2/R3. The team user confirms human authorship, author permission for datathon use/sharing, fluent independent review and reviewer non-authorship. These are team attestations, not an independent audit by the coding assistant. Exact review dates and dialect/variety details were not supplied. No synthetic or English practice records are claimed as Kikuyu contribution data. English glosses live separately in `data/reviewed_with_glosses.csv` and are never model input.

The new experiment uses **230 train / 50 dev / 50 test**. Each label has 23/5/5 records. All 50 test records come from the new 80-record extension and were absent from the original 250-model experiment. NFC/casefold lexical pairs at similarity ≥0.85 are kept together as connected families; semantic paraphrase leakage cannot be ruled out. Deterministic split selection used no model predictions. Original test records may now be train/dev: this is a new experiment with a wholly new holdout. See `EXPERIMENT_PROTOCOL.json`, `data/split_manifest.csv` and `data/related_pairs.csv`.

## Approach and measured results

We extracted the existing Colab baseline: character TF-IDF ngrams 2–5, then LogisticRegression(max_iter=1000, random_state=42). There was no hyperparameter search. The candidate was frozen before the new test was evaluated once. The browser performs real inference from the exported learned coefficients; it does not use hardcoded example responses or test-label lookup.

| Model on the SAME fresh 50-record test | Correct | Accuracy | Macro-F1 |
| --- | ---: | ---: | ---: |
| Original frozen 250-record experiment model | 36/50 | 72% | 0.7149 |
| Final 330-record experiment model | 40/50 | 80% | 0.7972 |
| Most-frequent baseline | 5/50 | 10% | 0.0182 |

The extension improved accuracy by eight percentage points on this test. The original model's historical 49/50 (98%) result belongs to a different older test; it is archived under `artifacts/baseline_250` and is not the 330-record result. There are ten final errors. Per-label reports, confusion matrix, actual predictions, five observed error examples, freeze hashes and same-test comparison are in `artifacts/intent/`. The small, one-author new holdout is not field validation. No tuning followed test inspection.

## Run and inspect

Python 3.10+; the actual run used Python 3.12 and scikit-learn 1.7.2. From this directory:

```text
python -m pip install -r requirements.txt
python validate.py --data data/contribution.csv --track intent
python -m http.server 8000 --directory web
```

Open http://localhost:8000 for the same static browser app. Inputs stay in the browser. It needs no API key. The hosted copy additionally contains the video asset; this repository links it rather than committing raw video. Only load trusted joblib files. To reproduce the frozen training in a separate working copy (it overwrites artifacts):

```text
python train.py --data data/contribution.csv --track intent
python evaluate.py --data data/contribution.csv --track intent
```

`tools/` contains the actual split, training/freeze/comparison and export helpers, plus the 334-case parity check. The experiment runner refuses to overwrite an existing final test result; use a separate clean working copy to reproduce. `run.log` is the observed run. The unchanged notebook snapshot is `notebooks/Team13_User_Edited_Colab.ipynb` (SHA256 in experiment protocol). We did not rewrite the live Colab's terms or text. Its embedded historical 250 experiment is retained as-is; the final 330 experiment is documented here separately.

## Limits, rights and credit

The model always chooses one of ten intents, including for unrelated input. Scores are uncalibrated. Spelling/variety coverage and semantic duplicate detection remain limited; see [QUALITY.md](QUALITY.md). Human review is team-confirmed. No public CC licence is invented: the dataset has the stated author permission for datathon use and sharing; code licensing is separate in `LICENSE_CODE.txt`.

Strathmore NLP Hub Starter Kit v2 provides the baseline and taxonomy. AI assistance (Codex/ChatGPT) was used for importing supplied data, split/code implementation and execution . It did not independently author, translate or verify the Kikuyu sentences. See [CONTRIBUTIONS.md](CONTRIBUTIONS.md), [DATA_CARD.md](DATA_CARD.md), [SOURCES.md](SOURCES.md), [REVIEW_CONFIRMATION.md](REVIEW_CONFIRMATION.md), and the row-level source/review logs. Additional size alone is not a claim to higher marks; the same-test comparison and deployable browser inference are the measured additions.
