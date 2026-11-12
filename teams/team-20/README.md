# Team 20 | Rada

## Team and task

- **Language:** written Kiswahili and Sheng, including English code-switching.
- **Track:** A — intent classification.
- **Original team repository:** https://github.com/Annah-2003/sheng-intent
- **Full source commit:** [bc98c8ada8e04e0347090a1f77ba0d6fae6addb2](https://github.com/Annah-2003/sheng-intent/commit/bc98c8ada8e04e0347090a1f77ba0d6fae6addb2)

We used [ClickUp](https://app.clickup.com/9012897541/v/s/901211092343) to assign tasks and track our progress.

**Data Lead — Kathy Auma**

Coordinates collection, reviews the wording and intent labels, and maintains the review decisions.

**Model Lead — Hafswa Sufi**

Prepares the data and splits, trains and evaluates the model, and builds the demonstration interface.

**Documentation Lead — Irene Gitau**

Brings the report sections together and checks the sources, results, run instructions and submission checklist.

AI assistance and the team's contribution statement are recorded in [docs/TEAM.md](docs/TEAM.md).

## Idea and approach

People should be able to approach useful digital tools in the language they use. We wanted to see whether a small model could recognise everyday requests written in Kiswahili and Sheng, including mixed wording such as “Nichezee doba”.

Rada identifies ten request types, including music, weather, alarms, calendars and lists. This is an assessment prototype. It shows a predicted category and a simulated response; it does not perform real actions.

1. Asked people what they would say to an assistant in everyday situations.
2. Reviewed their wording and labels; kept **324 human-written examples**.
3. Used **213 for training, 55 for development and 56 for the final test**. Related scenario groups stayed together.
4. Compared our data alone with adding 200 or 500 Kiswahili training examples from MASSIVE. We selected the version with 500 additional examples.
5. Selected the best development version, froze it and ran the final test once.

The organiser kit supplied the ten labels and starting model. We contributed the collected data, review work, experiment and demonstration. MASSIVE examples are counted separately.

## Data and review

Our final contribution contains **324 human-written examples: 213 training, 55 development and 56 test**. All ten intents meet the minimum of 15 training, five development and five test examples. We kept related scenario groups together; respondents can appear in more than one split.

We matched responses to the review workbook by source row and scenario, applied human decisions, preserved natural spelling and checked duplicates, contact patterns, labels and split counts. All test records have independent-review status. The main review was completed by one fluent reviewer, with follow-up decisions recorded separately. Some accepted labels remain ambiguous, and 15 original rejection reasons were not recorded.

The [cleaning and review report](docs/QUALITY_REPORT.md) links the spreadsheets in order, from collection to the final export. Our [annotation guide](ANNOTATION_GUIDE.md) contains the labelling rules; its original [version 1.1](docs/history/ANNOTATION_GUIDE_v1.1.md) is preserved. Source versions, terms and transformations are recorded in the [source log](docs/SOURCE_LOG.csv) and [dataset card](docs/DATASET_CARD.md).

## Code and how to run

Use Python 3.12 from the project folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The saved model is included; no API key or retraining is needed. [Validation, training, evaluation and test commands](docs/REPRODUCIBILITY.md).

The interface is in [app.py](app.py); preparation, training and evaluation code is in [src/](src/), with a [training notebook](notebooks/Training.ipynb). The saved models are in [models/](models/). Dependencies are listed in [requirements.txt](requirements.txt), with the original versions in [requirements-lock.txt](requirements-lock.txt).

The linked reproduction instructions cover dataset retrieval, validation, separate reconstruction and where outputs are saved. Keep the submitted experiment unchanged when reconstructing it.

## Results and limitations

**Final test: 43/56 correct — 76.8% accuracy, macro-F1 0.764.** Macro-F1 gives each category equal importance. Always guessing the most common training category gave 8.9% accuracy.

On development data, adding 500 MASSIVE examples increased correct predictions from 42/55 to 44/55. This is not a measured final-test improvement over the team-only model.

The sample is small. Some labels are debatable, some requests need context, and the same respondent can appear in different splits. Rada also forces unsupported requests into a known category. We have not measured real-world usability or improved access. [Results and five errors](docs/RESULTS.md).

Full outputs: [development comparison](reports/development.json), [final test metrics](reports/test.json), [per-intent results](reports/per_intent_test.csv), [confusion matrix](reports/confusion_matrix.csv) and [test predictions](https://github.com/Annah-2003/sheng-intent/blob/main/assessment/reports/test_predictions.csv).

## Presentation and demo video

- [Presentation and demo video folder](https://drive.google.com/drive/folders/1i1df1u6QQKMaxye50ZqwFpT_Ttq78b8a?usp=sharing)
- [Live prototype](https://sheng-intent-3nkn9auhiujhbpwvvwirby.streamlit.app/)

Our [design explanation](docs/HCI_DESIGN.md) connects the prototype interaction to the goal, action and feedback stages.

## Required materials

| Material | File or link |
| --- | --- |
| Contribution dataset and splits | [324-record CSV](https://github.com/Annah-2003/sheng-intent/blob/main/assessment/data/contribution.csv) and [per-intent split counts](reports/split_counts.csv) |
| Annotation guide | [Final guide](ANNOTATION_GUIDE.md) |
| Source log and terms | [Source log](docs/SOURCE_LOG.csv) and [MASSIVE licence](docs/licenses/MASSIVE.txt) |
| Dataset card | [Dataset card](docs/DATASET_CARD.md) |
| Quality and review evidence | [Cleaning and review report](docs/QUALITY_REPORT.md) and [spreadsheets and logs](https://github.com/Annah-2003/sheng-intent/tree/main/assessment) |
| Contribution and AI-use statement | [Team statement](docs/TEAM.md) |
| Evaluation and baseline comparison | [Results and five errors](docs/RESULTS.md), [development](reports/development.json) and [test](reports/test.json) outputs |
| Runnable code and dependencies | [Source](src/), [app](app.py) and [requirements](requirements.txt) |
| Trained artefacts and reproduction | [Models](models/) and [instructions](docs/REPRODUCIBILITY.md) |
| Presentation/demo video | [Recording](https://drive.google.com/drive/folders/1i1df1u6QQKMaxye50ZqwFpT_Ttq78b8a?usp=sharing) |

## Attribution and permissions

The organiser starter code retains its [MIT notice](LICENSE_CODE.txt). MASSIVE 1.1 Kiswahili training data is [CC BY 4.0](docs/licenses/MASSIVE.txt); its examples are separate from our human contribution. The photograph is CC BY-SA 4.0 with [photographer and source credit](assets/PHOTO_CREDIT.md).

We are sharing our collected contribution for datathon assessment; we have not assigned it a separate open-data licence. Private permission evidence is excluded from this submission folder. Reused material and AI assistance are disclosed in our [team statement](docs/TEAM.md).
