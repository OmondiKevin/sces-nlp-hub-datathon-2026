# Team 19 | Kiswahili intent recognition for phone-assistant requests

## Team and task

- Team number and name: Team 19
- Members and contributions:
  - Harry Sigei (GitHub: HSigei, `T19-A`): data lead, wrote dataset sentences (with Michael), rewrote flagged rows, model training, evaluation and demo.
  - Ezra Ntwiga (`T19-EN`): independent reviewer of all 50 test sentences; wrote no dataset sentences.
  - Michael Majau: wrote dataset sentences (with Harry) and rewrote flagged rows during review.
- Working language/variety: Kiswahili as spoken in Kenya (`sw-KE`), including everyday Sheng and Kiswahili–English code-switching.
- Track: A, intent classification (10 MASSIVE-aligned labels in [taxonomy.csv](taxonomy.csv)).
- Original team repository URL: https://github.com/HSigei/team19-kiswahili-intent
- Full source commit SHA for the version submitted: `60ef75113ec2fd29608ea8cee03bad635b12f2fa` (tag `submission-v1`)

## Idea and approach

Phone assistants rarely understand the way Kenyans actually ask for things: Kiswahili mixed with Sheng and English ("Nipee time", "Seti alarm ya saa kumi", "niwekee wimbo aina ya bongo"). We built a small, original, human-written Kiswahili dataset of assistant requests and a classifier that maps each request to one of 10 intents (weather, time/date, alarms, calendar, lists, music, news, definitions).

1. Team members wrote original Kiswahili/Sheng requests for each label (Route B, `source_method = original_human`) in a shared record template.
2. We reviewed every record of the first draft against the label boundaries in the [annotation guide](docs/ANNOTATION_GUIDE.md). Records that did not express their label (date questions filed as calendar_set, alarm volume/snooze complaints filed as alarm_set, comments filed as news_query, empty and duplicate rows) were flagged with a written reason, and team members rewrote 83 of them as new requests for the intended label; 11 more had spelling or formatting fixed. Every change, with the first-draft text and the reason, is in [data/review_changes.csv](data/review_changes.csv), and [team19_final.py](team19_final.py) rebuilds the dataset from the spreadsheets in `data/source/`.
3. We trained the starter kit's character n-gram (2–5) TF-IDF + logistic regression model, which copes well with Sheng spelling variation, and compared it with a majority-class baseline.
4. We evaluated once on the frozen, independently reviewed test split and demo the model in the Streamlit app.

New: the Kiswahili dataset, its review, and the build/cleaning script. Reused: the Strathmore NLP Hub starter kit code (validate/train/evaluate/app).

## Data and review

Accepted records: **250** (final). Source methods: {'original_human': 250}. Review status: {'self_reviewed': 200, 'independently_reviewed': 50}.

| Label | train | dev | test | total |
|---|---|---|---|---|
| weather_query | 15 | 5 | 5 | 25 |
| datetime_query | 15 | 5 | 5 | 25 |
| alarm_set | 15 | 5 | 5 | 25 |
| calendar_set | 15 | 5 | 5 | 25 |
| calendar_query | 15 | 5 | 5 | 25 |
| lists_createoradd | 15 | 5 | 5 | 25 |
| lists_query | 15 | 5 | 5 | 25 |
| play_music | 15 | 5 | 5 | 25 |
| news_query | 15 | 5 | 5 | 25 |
| qa_definition | 15 | 5 | 5 | 25 |

- Contribution data and splits: [data/contribution.csv](data/)
- Original working spreadsheet: [data/source/](data/source/)
- Annotation guide: [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md) · Data card and source log: [docs/DATA_CARD.md](docs/DATA_CARD.md) · Quality report: [docs/QUALITY.md](docs/QUALITY.md) · Data plan: [docs/DATA_PLAN.md](docs/DATA_PLAN.md)
- Each record has its own `group_id`; the validator checks that no group crosses splits and that text is not duplicated after normalisation.
- Every test record was independently reviewed by Ezra Ntwiga (`T19-EN`), a Kiswahili speaker. Ezra wrote none of the sentences.

## Code and how to run

Python 3.12; dependencies in [requirements.txt](requirements.txt) (scikit-learn 1.7.2, pandas, streamlit, joblib).

```
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt openpyxl
python validate.py --track intent --data data/contribution.csv
python train.py    --track intent --data data/contribution.csv
python evaluate.py --track intent --data data/contribution.csv
streamlit run team19_app.py
```

Outputs are written to `artifacts/intent/` (model.joblib, dev_metrics.json, test_metrics.json, per_label_report.csv, test_predictions.csv). The model file is not committed; the commands above rebuild it in seconds. `python team19_final.py` rebuilds `data/contribution.csv` from the reviewed spreadsheet in `data/source/` and reruns validate, train and evaluate.

## Results and limitations

Frozen test set (50 sentences): **accuracy 0.900, macro-F1 0.899** vs majority-class baseline macro-F1 0.018. Dev macro-F1 0.918. Per-label scores: [results/per_label_report.csv](results/per_label_report.csv); predictions: [results/test_predictions.csv](results/test_predictions.csv).

Actual test errors:

1. "Ongeza mafunzo ya kompyuta Alhamisi saa mbili asubuhi.": expected `calendar_set`, predicted `alarm_set`. Contains a time phrase ("saa mbili asubuhi") that is far more frequent in alarm sentences, and no calendar word (kalenda/mkutano) the model relies on.
2. "Naomba uanzishe orodha ya vifaa nitakavyohitaji chuoni.": expected `lists_createoradd`, predicted `lists_query`. Both list labels share "orodha"; the create verb "uanzishe" is rare in training, so character n-grams cannot separate the two.
3. "Tafadhali andika kufua nguo kwenye orodha yangu ya kazi za kesho.": expected `lists_createoradd`, predicted `lists_query`. "orodha yangu" appears mostly in questions about lists; the add verb "andika" is underweighted.
4. "Je, nilijumuisha unga wa ngano kwenye orodha ya sokoni?": expected `lists_query`, predicted `lists_createoradd`. "nilijumuisha ... kwenye orodha" looks like an add request on the surface; the question form (Je, ...?) is a weak signal for a bag-of-n-grams model.
5. "Tafsiri ya istilahi biometriki ni nini?": expected `qa_definition`, predicted `datetime_query`. Unseen technical words ("istilahi", "biometriki") give no qa_definition signal, and "ni nini?" alone is shared with time/date questions.

Limitations:
- Small dataset (about 25 sentences per label) written by a few people, so it covers a narrow range of speakers, regions and topics.
- Character n-grams match surface spelling; requests with unusual wording or unseen Sheng may be misclassified.
- The model always picks one of the 10 labels, even for out-of-scope requests (e.g. volume or stop commands, which we excluded from the data).
- The demo simulates routing only; no alarm, calendar or music action is executed.

## Presentation and demo video

- Presentation/demo video URL (REQUIRED): https://team19-video.pages.dev
- Optional hosted app URL: none

## Required materials

- Contribution dataset and splits: [data/](data/)
- Annotation guide: [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md)
- Source log and source terms: [docs/DATA_CARD.md](docs/DATA_CARD.md), [data/review_changes.csv](data/review_changes.csv)
- Dataset card: [docs/DATA_CARD.md](docs/DATA_CARD.md)
- Quality/review report: [docs/QUALITY.md](docs/QUALITY.md)
- Contribution and AI-use statement: [docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md)
- Evaluation outputs and baseline comparison: [results/](results/)
- Runnable code and dependency file: [team19_app.py](team19_app.py) (styled Team 19 demo; app.py is the original starter-kit demo), [train.py](train.py), [evaluate.py](evaluate.py), [validate.py](validate.py), [requirements.txt](requirements.txt)
- Trained artefacts or reproduction instructions: see "Code and how to run"
- Video link: see above

## Attribution and permissions

Code is adapted from the Strathmore NLP Hub Datathon 2026 starter kit (see [LICENSE_CODE.txt](LICENSE_CODE.txt)). Label set aligned with the MASSIVE intent taxonomy. All sentences were written by Team 19 members, who agreed to their use for this datathon; permission evidence is held privately. Licence for our data: CC-BY-4.0 (team members consented to its use). AI assistance (Claude, Anthropic) was used for review support, cleaning scripts and documentation, as described in [docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md); it did not write dataset sentences.
