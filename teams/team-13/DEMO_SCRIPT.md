# Team 13: three-speaker demo script (about 2 minutes 40 seconds)

Record your real voices. Show the public app while Celestine speaks. These are suggested speaking sections, not claims that a speaker personally wrote the code or authored particular records. The existing backup video is captioned and automated, with no human narration.

## Nadine Njora — introduction and purpose (0:00–0:35)
Hello, we are Team 13, Kikuyu 2: Nadine Njora, Wanyingi Shirleen Muthoni and Celestine Nyingi. Our Track A project recognises what a person is asking in Kikuyu and routes the request to one of ten fixed intents, such as weather, alarms, lists and music. This prototype displays the predicted intent. It does not execute actions. We wanted a small, inspectable language project with honest evaluation and a demo judges can open without signing in. Shirleen will explain the data.

## Wanyingi Shirleen Muthoni — data and review (0:35–1:20)
Our submitted dataset contains 330 sentences, with 33 in each intent. We supplied the sentences and confirmed human authorship under author codes A1, A2 and A3. Fluent reviewers R1, R2 and R3 checked the corresponding batches independently and wrote none of the sentences they reviewed. Authors permitted datathon use and sharing. Our logs record these team confirmations; exact review dates and dialect details were not supplied. We kept the Kikuyu wording and separated the English glosses from model input. Related lexical families stay in the same split. The final split is 230 training, 50 development and 50 entirely new test records from the 80-sentence extension.

## Celestine Nyingi — model, live demo and results (1:20–2:25)
We retained the baseline from our existing Colab: character TF-IDF features from two to five characters and logistic regression. We froze the settings and model before evaluating the new test. The final model correctly classified 40 of 50 new sentences: 80 percent accuracy and macro-F1 of 0.797. The original 250-record model scored 36 of 50, or 72 percent, on those same new sentences. This is an eight percentage point improvement, not a comparison with our historical 98 percent score on a different test.

[Open the public app. Click the music example, then Classify request if needed.]
Here is an actual prediction from the trained model. The displayed probability is uncalibrated and does not guarantee correctness. We also checked that the browser model matches Python predictions on 334 parity cases.

[Enter ??? and classify.]
An unsupported input still receives one of the ten classes. The warning shows why this is a prototype and why a rejection option is future work. With only five test records per intent from one author, these results cannot establish general Kikuyu understanding.

## Nadine — closing and credits (2:25–2:40)
Our repository includes the permitted data, review logs, frozen model, predictions and error analysis. We credit Strathmore NLP Hub Starter Kit v2 and disclose AI assistance for code, testing, documentation and this captioned backup. Our user-edited Colab wording is preserved. Thank you.
