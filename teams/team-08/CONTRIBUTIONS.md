# Contributions and AI use

## Members

Wayne Kimutai: code and demo. Ran validation, training, evaluation and the Streamlit demo; produced the submission, repository and video. Evidence: repository commits and artifacts/semantic/.
Grace Wangari: language reviewer. Reviewed Kiswahili wording, intents and slots. Evidence: review_status and reviewer_code in data/contribution.csv [CONFIRM RECORD IDS OR COUNT].
Joy Tele: data and documentation. Maintained the annotation spreadsheet, annotation guide, data card and quality report. Evidence: spreadsheet history and the documents in this folder.
[ADD ANY OTHER WRITERS AND WHICH writer_id (G1, G2, G3) THEY ARE.]

## Upstream code reused

Strathmore NLP Hub Datathon starter kit v2.0: train.py, evaluate.py, validate.py, core.py, app.py, taxonomy.csv, templates. Used unchanged except for data paths. License: see LICENSE_CODE.txt.

## AI tools used

Claude (Anthropic), auditing the annotation spreadsheet for duplicates, mislabelled intents, spelling and span errors and rule conflicts.
Writing a script that converts the spreadsheet to contribution.csv, computes character offsets and assigns splits

The Kiswahili sentences were written by the team. AI was not used to generate or rephrase the text of the records. AI identified problematic rows and the team wrote the replacement sentences. For that reason ai_declared is "no" for the sentences.

## Human checks applied

The team reviewed slots and corrected errors found by validate.py (span typos, case mismatches). The language reviewer checked the language and meaning [CONFIRM SCOPE]. Metrics are copied from the files produced by evaluate.py.

## Suggestions rejected

[CONFIRM OR EDIT: relabel all Nikumbushe reminder requests as calendar_set was not followed; the team kept them as alarm requests, reworded as Weka kengele.]

