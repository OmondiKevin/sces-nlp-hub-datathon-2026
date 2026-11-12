# Data plan

**Team 14 (Maa)** | Strathmore NLP Hub Datathon 2026
Members: Philip Tait, Neema Mapelu Naserian, Mayabi Muigai Ivan

## Team, task, language and variety
- Task: Track A, intent classification. We use the 10 labels in `data/taxonomy.csv`.
- Language: Maa (Maasai).
- Variety: mixed. Our contributors come from different Maa communities (for example around Kajiado and Narok), so we don't claim one standard variety. A wording from another community is not counted as a mistake.
- Language code for the CSV: `mas` (Maasai, ISO 639-3)

## Reviewer and capacity
- Reviewer: R01. A native Maa speaker from Narok County whose mother tongue is Maa (Illukumae variety), fluent in speaking and
  writing Maa. R01 is a relative of a team member and did not fill in the form.
- How much they can review and by when: all 1,247 raw answers, including every answer behind the 165 final test records, completed
  on 11 November 2026 before cleaning.
- A reviewer can't review text they wrote themselves.
- Contact details stay private and are not in the repo.

## Data source
We collected our own data (Route B). Existing sources for Maa were not reliable enough, so we didn't use them. MASSIVE is only used for the label names.

We made a Google Form with 20 everyday situations in English, two for each intent. Contributors wrote what they would say in Maa, in their own words, and could add a second way of saying it. We didn't give them sentences to translate. We asked for fluent Maa speakers who can write Maa, and the form asked how well each person speaks and writes it.

The form was open from 9 to 11 November 2026. R01 reviewed the export of 41 responses. A few responses arrived after R01's review, the cleaning and the model training, and they are not in the dataset.

Each contributor read a short notice (data used for the datathon and possible NLP Hub review, credited by code only, write it yourself with no machine translation or AI) and ticked a box saying they were 18 or older and agreed to take part. The consent records stay in our private response sheet, not on GitHub.

## Contribution type and target
- Type: original human-written examples.
- Target: at least 250 accepted records, 25 per intent (15 train, 5 dev, 5 test).
- Only records the reviewer accepts go into `data/contribution.csv`. Anything not reviewed stays out.

## Labels and edge cases
The 10 labels are weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query and qa_definition.

The label of each answer comes from the situation it answers, so the reviewer has to confirm it. If it's wrong we correct it or drop it.

Intents that can get mixed up: weather vs news, alarm vs calendar event, adding to a list vs reading it, calendar_set vs calendar_query, playing music vs asking about a song, and a definition vs a general fact question.

We leave out answers that ask for two things, unclear answers, and anything with personal details. Words borrowed from Swahili or English are kept if people really say them that way.

## Splits and review
Splits were made by contributor and intent (group_id is contributor plus intent), so the same contributor can appear in train, dev and test. Because of this, test scores may be optimistic. R01 reviewed all raw answers before the split, so every test record comes from an answer R01 checked.

## Who does what
- Philip: Google Form, data collection, repo, documentation
- Neema: data quality review
- Ivan: model training, evaluation and the Streamlit demo
- External reviewer (R01): language review. Confirmed: R01 completed the review.

## Risks
- R01 is a relative of a team member and was the only reviewer, so nobody checked R01's review. The review was done on the raw export before cleaning and normalisation, so R01 did not see the final text.
- Mixed varieties and borrowed words make some answers hard to judge.
- The repo is private. Raw responses and consent records are kept outside it.
- Everything runs on CPU only.

## Organiser confirmation
None received as of 12 November 2026.
