# Team 04 | SautiByte - Kiswahili Intent Classification

## Team and task
- **Team number and name:** Team 04 (SautiByte)
- **Three members and their contributions:** 
  - Omwoyo Leo Kinara (T04-L): Authored 84 records, peer review, documentation.
  - Daniel Brian Kikuvi (T04-B): Authored 83 records, peer review, quality report.
  - Zakariya Mohamed (T04-Z): Authored 83 records, peer review, model training, recorded demo.
- **Working language/variety:** Kiswahili (`sw-KE`, Kenyan variety with Sheng and code-switching)
- **Track:** A intent
- **Original team repository URL:** [https://github.com/lolkao55/SautiByte-NLP26]
- **Full source commit SHA for the version submitted:** [e2b38ca54c600a59dc285ca1a9b56538da27798d]

## Idea and approach
Our goal was to build an intent classification model for smart assistants that understands real-world Kenyan Kiswahili, mapping natural commands to 10 distinct action labels. Users would use this to seamlessly control apps (weather, alarms, lists, calendars, music) using the casual, code-mixed language they speak daily, rather than rigid standard translations.
**Steps taken:**
1. Authored 250 original Kiswahili sentences incorporating natural Sheng (e.g., "ngoma", "playlist").
2. Conducted independent peer-reviews on all test records to ensure natural quality and correct intent mapping.
3. Formatted data into exact 15/5/5 train/dev/test splits per label.
4. Trained the baseline character TF-IDF and logistic regression model using the Datathon starter kit.
5. Deployed the model locally using Streamlit to demonstrate real-time predictions.

## Data and review
- **Accepted contributions:** 250 `original_human` records (`source_dataset = team_authored`).
- **Coverage:** 25 records exactly per label (weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query, qa_definition).
- **Splits:** 150 Train / 50 Dev / 50 Test.
- **Review method:** All 50 test records (and train/dev sets) were independently reviewed by a team member who did not author them (e.g., T04-L's records were reviewed by T04-B).
- **Quality checks:** Validated structural requirements via `validate.py` (PASS: 250 records). Corrections to spelling and ambiguous intents were resolved and documented.

## Code and how to run
**Requirements:** Python 3.10+, Streamlit, and standard starter kit dependencies.
**Commands:**
1. Activate virtual environment: `.venv\Scripts\activate.bat` (or `.ps1` for PowerShell)
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Validate: `python validate.py --track intent --data data/contribution.csv`
4. Train: `python train.py --track intent --data data/contribution.csv`
5. Evaluate: `python evaluate.py --track intent --data data/contribution.csv`
6. Run UI: `python -m streamlit run app.py`
*(Artefacts including `.joblib` model and JSON/CSV reports are generated and written to `artifacts/intent/`)*

## Results and limitations
- **Final frozen test Accuracy:** 0.860 (86.0%)
- **Final frozen test Macro-F1:** 0.858
**Limitations:**
1. **Unseen Vocabulary:** The model failed on words missing from training (e.g., missed "hali ya hewa", relying instead on time anchors like "wikendi").
2. **Shared Trigger Words:** The model confused commands starting with "Weka" (used both for scheduling calendars and playing music).
3. **Character fragment overlap:** Falsely predicted `lists_query` for the word "playlist" due to the shared "list" character fragment.

## Presentation and demo video
- **Presentation/demo video URL (REQUIRED):** [[https://drive.google.com/file/d/1VNOoZLsmsSufe2ilpT0O2Ab4tLuNjwco/view?usp=sharing]]

## Required materials
- **Contribution dataset and splits:** `data/contribution.csv`
- **Annotation guide:** `documentation/ANNOTATION_GUIDE.md`
- **Dataset card:** `documentation/DATA_PLAN.md`
- **Quality/review report:** `documentation/quality_report.md`
- **Evaluation outputs and baseline comparison:** `artifacts/intent/`
- **Runnable code and dependency file:** `app.py`, `train.py`, `evaluate.py`, `requirements.txt`
- **Trained artefacts or reproduction instructions:** `artifacts/intent/`
- **Video link:** [https://drive.google.com/file/d/1VNOoZLsmsSufe2ilpT0O2Ab4tLuNjwco/view?usp=sharing]

## Attribution and permissions
All starter code, baseline models, and evaluation scripts were provided by the Strathmore NLP Hub Datathon starter kit v2.0. Our Kiswahili dataset (`sw-KE`) is 100% original human-authored data created specifically for this competition by Team 04. No upstream datasets or bulk AI translations were utilized.


