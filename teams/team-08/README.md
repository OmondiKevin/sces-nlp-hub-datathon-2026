# Team 8 (Verity): Kiswahili limited semantic parsing (Track C)

Strathmore NLP Hub Datathon 2026. Language: Kiswahili. Task: Track C, limited semantic parsing.

Demo and presentation video (2-3 minutes): https://drive.google.com/file/d/1444-QGdfI7e5wTg-AGOl8L7WbHCRFSb9/view?usp=sharing
Team repository: [TEAM REPOSITORY URL]
Frozen commit SHA: [FULL 40-CHARACTER SHA FROM git rev-parse HEAD]

## Idea

An assistant for people who write in Kiswahili has to work out what the person wants and then pick out the details, such as the place, the date and the time. For example, "Niamshe saa kumi na mbili asubuhi kesho" should become an alarm request with a time slot and a date slot. The system only shows the recognised action and slots as JSON. It does not perform real actions.

## Approach

We wrote 250 Kiswahili requests ourselves, 25 for each of the ten actions in the starter taxonomy: weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query and qa_definition. 193 of the 250 requests carry at least one slot. Slot types are location, date, time, item and term. Offsets are Python Unicode character indices, start inclusive and end exclusive, and a script computes them from the text so that text[start:end] equals the value.

The data is split 150 train, 50 dev and 50 test (15, 5 and 5 per action). Requests that are paraphrases of one situation share a group_id so they stay in one split. The model is the unmodified starter baseline: character n-gram TF-IDF with logistic regression chooses the action, and a dictionary of surface values memorised from the training split finds slots. We did not change the model and did not tune on the test set.

## Results on the frozen test set (50 examples, evaluated once)

Action accuracy 0.74. Macro-F1 0.732. Majority-class baseline: accuracy 0.10, macro-F1 0.018.
Slot type and span: precision 0.741, recall 0.351, F1 0.476.
Full-frame exact match (right action and the complete slot set): 0.32.
Unseen-value subset (24 test examples containing a slot value never seen in training): slot F1 0.196, full-frame exact match 0.0.
Weakest action: calendar_query (F1 0.286), usually mistaken for datetime_query. Strongest: news_query (F1 1.0).
Files: artifacts/semantic/test_metrics.json, per_label_report.csv, test_predictions.csv. Five analysed errors are in QUALITY.md.

## Limitations

The dataset is small, and the test set has only 50 examples, so differences of a few examples move the scores a lot. The slot finder can only recognise values it has seen in training, so it fails on new places, event titles, dates and topics. Several label boundaries are close (calendar_query against datetime_query, lists_query against lists_createoradd). Annotation rules for item and term slots are team conventions, not a confirmed standard. See QUALITY.md and DATA_CARD.md.

## How to run

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python validate.py --track semantic --data data/contribution.csv
python train.py --track semantic --data data/contribution.csv
python evaluate.py --track semantic --data data/contribution.csv
python -m streamlit run app.py

data/make_contribution.py rebuilds data/contribution.csv from the annotation spreadsheet, with a fixed random seed for the split.

## Team contributions

Wayne Kimutai: code and demo (training, evaluation, Streamlit app, conversion script, submission and video).
Grace Wangari: language review of the Kiswahili text, intents and slots.
Joy Tele: data and documentation (annotation spreadsheet, guide, data card, quality report).
Contribution and AI-use details are in CONTRIBUTIONS.md.

## Documents

ANNOTATION_GUIDE.md, DATA_CARD.md, QUALITY.md, CONTRIBUTIONS.md.

Starter code and taxonomy are from the Strathmore NLP Hub Datathon starter kit v2.
