# Quality report

**Team 16 / Kinyarwanda sentiment / working revision 1.3**  
**Snapshot:** 10 November 2026

## Contributions and splits

The contribution file has 345 rows: 30 `original_human`, 199 `human_localised`, and 116 `llm_generated`. All synthetic rows are in train. The file contains no rows attributed to an external dataset. `data/other.csv` and `data/other2.csv` are separate raw files with no source/licence documentation in the repository; they are not counted here.

| Label | Train | Test | Dev | Total |
|---|---:|---:|---:|---:|
| Negative | 69 | 23 | 23 | 115 |
| Positive | 69 | 23 | 20 | 112 |
| Neutral | 69 | 23 | 26 | 118 |

The five human label corrections changed the class totals and dev balance. Do not describe the current file as exactly 1:1:1 or 60/20/20 per class.

## Independent review

The CSV marks all 345 rows as `independently_reviewed` and assigns `reviewer_001` and the plan maps that code to `Innocent Mukiza`. 

## Disagreements and resolutions

The native-speaker feedback resolved five model-confusing examples:

| Record ID | Record | Original Label | Reviewer Label |  Action Taken  |
|---|---|---|---|---|
| `kin-015` | Byose byagenze nk’uko byari biteganyijwe. | Positive	| Neutral |Changed positive to neutral: the sentence reports that events went as planned without explicit emotional wording. |
| `kin-155` | Ibyo badusezeranyije byose byabaye imfabusa ku munota wa nyuma. | Positive	| Negative | Changed positive to negative. The reviewer accepted `byabaye imfabusa` as idiomatic but flagged `ku munota wa nyuma` as a possible English calque. That part was left as-is |
| `kin-314` | Ubufatanye bwiza bwagaragajwe bwatumye twose twishima.	 | Negative | Positive | Changed negative to positive, corrected `twose` to `twese`, and adopted a more conversational wording: `Twafatanyije neza kandi twese byaradushimishije.` |
| `kin-319` | Inyandiko yacu igizwe n'ibice bitandatu byose hamwe. | Positive | Neutral | Changed positive to neutral: it is a factual description of a document. |
| `kin-327` | Igiciro cy'ibiribwa cyagumye ku rugero rumwe muri uku kwezi. | Positive | Neutral | Changed positive to neutral: stable food prices are not explicitly praised or criticized. |



The exact model predictions for the first training on the initial dataset(v1.2) with the settings: char, LinearSVC, C=1.0 was as follows with the values that are listed being the ones that the model misclassified.
| text |  actual label | model predicted |
|---|---|---|
| Uyu mwanzuro watumye habaho igihombo gikomeye cyane. | negative | positive |
| Abateguye iri rushanwa ntibubahirije amategeko bari batangaje. | negative  | positive |
| Uko yansubije imbere y'abandi bantu byanyeretse ko atanyubaha. | negative  | positive |
| Twahuye nimbogamizi nyinshi cyane zitari zikenewe na gato. | negative |  positive |
| Ubufatanye bwiza bwagaragajwe bwatumye twose twishima. | negative | positive |
| Icyemezo cyafashwe cyatugizeho ingaruka mbi cyane. | negative | positive |
| Aya makuru yose twahawe ntagize icyo afasha mu byukuri. | negative | neutral |
| Imbonerahamwe y'amasaha y'akazi yamaze gushyirwa ahagaragara.  | neutral | negative |
| Mu gikoni hari ibikoresho byo guteka, amasahani n'ibikoresho byo kunyweraho.  | neutral  | negative |
| Ubufasha bwose twabonye bwatumye turangiza gahunda zacu vuba.  | neutral  | positive |
| Ubufatanye bwaranze itsinda ryacu bwatanze umusaruro utangaje.  | neutral  | positive |
| Ubumwe bwacu nibwo bwatugejeje kuri ubu bwiza bwose tubona.  | neutral  | positive |
| Iyi mashini nshya yorohereza abakozi imirimo ya buri munsi. | positive   | neutral |
| Igiciro cy'ibiribwa cyagumye ku rugero rumwe muri uku kwezi. | positive | neutral |
| Ibipimo by'ubuzima byakozwe ku bakozi bose bashya bageze aho. | positive | neutral |
| Twageze ku ntego zacu zose ku gihe. | positive | neutral |
| Inyandiko yacu igizwe n'ibice bitandatu byose hamwe. | positive | neutral |
| Ibyo badusezeranyije byose byabaye imfabusa ku munota wa nyuma. | positive | negative |
| Byose byagenze nk’uko byari biteganyijwe. | positive | negative |
| Dufite ishimonshi ku bw'intambwe nziza tumaze gutera. | positive  | negative


## Structural checks and data limits

A standard-library inspection on 10 November 2026 found 345 records, no blank fields, unique record IDs, no duplicate text after NFC/casefold/whitespace normalization, no `group_id` spanning multiple splits, and no `llm_generated` rows in dev or test. `validate.py` was not rerun for this report.

The current `group_id` convention encodes label and split (for example, `group_pos_dev`)

## Model and metrics

`train.py` specifies character TF-IDF with 2–5 character n-grams and `LinearSVC(C=1.0, random_state=42)`. It compares against a most-frequent-label `DummyClassifier` baseline.

This was chosen after different runs were done and the results compared as follows:

| Model | Split | Accuracy | Macro-F1 | Notes |
|---|---|---:|---:|---|
| Most-frequent-label `DummyClassifier` | Dev (69 rows) | 0.333 | 0.167 | Majority baseline |
| Character TF-IDF + `LogisticRegression(max_iter=1000,random_state=42)` | Dev (69 rows) | 0.7101 | 0.7092 | Initial configuration |
| Word TF-IDF + `LogisticRegression(max_iter=1000,random_state=42)` | Dev (69 rows) | 0.6667 | 0.6663 | Worst overall |
| Combined TF-IDF + `LogisticRegression(max_iter=1000,random_state=42)` | Dev (69 rows) | 0.6957 | 0.6962 | Stronger than the initial model on positive but weaker on neutral |
| Character TF-IDF + `LinearSVC(C=1.0, random_state=42)` | Dev (69 rows) | 0.7101 | 0.7105 | Selected configuration |
| Character TF-IDF + `LinearSVC(C=0.1, random_state=42)` | Dev (69 rows) | 0.7101 | 0.7092 | Negligible différence |
| Character TF-IDF + `LinearSVC(C=10.0, random_state=42)` | Dev (69 rows) | 0.6812 | 0.6799 | Selected |


We then trained the selected configuration on an AfriSenti subset only(90 records) as well as a combined dataset of the original dataset and the AfriSenti subset and found the following:
|Sentiment | Original | AfriSenti only | Combined |
|---|---|---|---|
| Positive F1 | 0.727 | 0.533 | 0.698 |
| Negative F1 | 0.773 | 0.286 | 0.791 |
| Neutral F1 | 0.800 | 0.372 | 0.808 |
| Macro-F1 | 0.767 | 0.397 | 0.765 |

The available `artifacts/dev_metrics.json` is an earlier snapshot with 69 dev rows and 23 examples per label: model accuracy **0.710**, macro-F1 **0.711**; majority baseline accuracy **0.333**, macro-F1 **0.167**. 

## Language variety 

The dataset is small, includes 116 synthetic training examples, and has no dialect, demographic, or domain tags. The native reviewer noted a formal written register in several examples. We'll need to broaden the range with natural everyday phrasing.

Overlapping records: 745
Same labels: 740
Different labels: 5
| text_single | label_single | label_annotated |
|---|---|---|
| Ark ubu neza neza nabuze umuntu uzanshyira mukiziga nukuri 😭😭😂🙆‍♂️ | negative | neutral |
| Bimwe mu bikizitiye abakobwa n’abagore mu ikoreshwa ry’ikoranabuhanga https://t.co/cdGf8MFpDG | negative | neutral |
| Batatu bafunzwe bakurikiranyweho kugerageza gutwika inyubako yo mu Gakiriro ka Gisozi https://t.co/ovEmLkDBlP | negative | neutral |
| Dr. Ugirashebuja Emmanuel yagizwe minisitiri w’ubutabera akaba n’intumwa nkuru ya Leta, ni umwanya agiyeho asimbuye Johnston Busingye https://t.co/XQvkLiR5E8 | positive | neutral |
| Gikukuru umuti ukomeye w'indwara nyinshi irwanya cancer, ikanakesha ibice by'umubiri bitandukanye #ITABAZA #ItabazaTV #RwOT #Burundi #Rwanda https://t.co/IXCwMVvspe | positive | neutral |