# Dataset Card: Team 11 Dholuo Sentiment Dataset

**Team:** Team 11 – NLP Hub Datathon 2026  
**Primary language:** Dholuo  
**Task:** Three-class sentiment classification  
**Dataset version:** Final contribution v1.0  
**Status:** Structurally validated; linguistic and source-rights limitations remain  
**Last updated:** 11 November 2026

## 1. Dataset overview

The Team 11 Dholuo Sentiment Dataset contains 300 text records intended for three-class sentiment classification in Dholuo.

Each record contains a text sample, a sentiment label and metadata describing its source, contribution method, review status and dataset split.

The dataset supports an experimental demonstration of sentiment classification for a low-resource African language. It is not a validated general-purpose Dholuo benchmark.

## 2. Intended task

The dataset supports sentence-level classification into:

- **Positive:** favourable opinions, approval, satisfaction or encouragement.
- **Negative:** unfavourable opinions, dissatisfaction, criticism or disappointment.
- **Neutral:** statements without clearly expressed positive or negative sentiment.

It is not designed to identify specific emotions, diagnose psychological conditions, detect sarcasm reliably or interpret complex conversations.

## 3. Language and variety

| Attribute | Description |
|---|---|
| Language | Dholuo |
| Language family | Nilotic |
| Geographic and linguistic context | Dholuo-speaking communities, particularly in Kenya and neighbouring regions |
| Text format | Written sentences |
| Dialect coverage | Not systematically documented |
| Code-switching | Not systematically assessed |

The dataset should not be assumed to represent every Dholuo dialect, speaker group or communication context.

## 4. Dataset structure

The contribution records use the following fields:

| Field | Description |
|---|---|
| Record ID | Unique identifier assigned to a dataset record |
| Language | Language associated with the text |
| Text | Dholuo sentence |
| Label | Positive, negative or neutral |
| Source Dataset | Original source or contribution category |
| Source Version | Source dataset version |
| Source Record ID | Original source record identifier, where available |
| Source URL | Source reference |
| Source Method | Method used to create or adapt the example |
| Licence or Permission | Recorded rights or permission information |
| Contributor Code | Identifier of the contributor |
| Reviewer Code | Identifier of the reviewer |
| Review Status | Recorded review status |
| Group ID | Grouping identifier used to prevent split leakage |
| Split | Training, development or test |

## 5. Final dataset composition

The final contribution dataset contains 300 records.

### Label distribution

| Label | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| **Total** | **300** |

### Split distribution

| Label | Training | Development | Test | Total |
|---|---:|---:|---:|---:|
| Positive | 60 | 20 | 20 | 100 |
| Negative | 60 | 20 | 20 | 100 |
| Neutral | 60 | 20 | 20 | 100 |
| **Total** | **180** | **60** | **60** | **300** |

### Contribution methods

All 300 records are derived from Sindhi source material. The recorded methods describe how the Dholuo text was produced.

| Source method | Records | Description |
|---|---:|---|
| `machine_translated` | 276 | Initial Dholuo drafts produced using Google Translate and used largely as translated |
| `human_localised` | 24 | Initial Google Translate drafts subsequently human-localised by the team |
| **Total** | **300** | |

These method labels should not be interpreted as proof of independent linguistic validation.

## 6. Data provenance and preparation

The original source material was obtained from a Sindhi-language dataset attributed to Ali Nawaz and listed on Mozilla Data Collective.

Google Translate was used to produce the initial Dholuo drafts for all 300 records from Sindhi source sentences. The resulting contribution methods are:

- 276 records retained the machine-translated output largely as produced.
- 24 records were subsequently human-localised.

The recorded contribution methods are `machine_translated` and `human_localised`. These labels describe the preparation process; they do not establish independent linguistic validation.

Because all records derive from Sindhi source material, the relationship between the original material and the resulting Dholuo text must remain documented.

The exact source version, record-level traceability and applicable derivative-data and redistribution terms require further confirmation. See `docs/provenance_and_rights.md`.

## 7. Annotation process

Each example is assigned one of three sentiment labels:

- Positive
- Negative
- Neutral

Annotation decisions should follow the accompanying `sentiment_guidelines.md`.

Ambiguous, unnatural or difficult-to-classify examples require careful review. Structural validation alone cannot establish that a Dholuo sentence is natural or that its sentiment label is linguistically correct.

## 8. Review status

Review metadata in the final contribution dataset records:

| Review status | Records |
|---|---:|
| Self-reviewed | 217 |
| Independently reviewed | 83 |
| **Total** | **300** |

All 60 held-out test records were independently reviewed. Their reviewer codes differ from their contributor codes.

The remaining records have varying review status. Therefore, the dataset should not be described as independently reviewed in its entirety.

Independent review metadata does not, by itself, establish broad agreement among fluent Dholuo speakers or comprehensive linguistic validation.

## 9. Data quality and validation

The final contribution CSV was checked for:

- 300 records.
- No missing required values.
- No duplicate record IDs.
- No duplicate normalised text entries.
- No group IDs spanning multiple dataset splits.
- The expected 180/60/60 split.
- Independent review of all 60 test records.

The official sentiment validator completed successfully:

```text
PASS: 300 records; language quality, permission and semantic duplicate review remain human responsibilities.
```

This result confirms that the dataset passed the validator's checks. It does not establish linguistic correctness, semantic fidelity, source permission or general suitability for Dholuo NLP research.

See `docs/data_quality_report.md` for the detailed audit.

## 10. Intended uses

Potential uses include:

- Educational demonstrations of Dholuo NLP.
- Experimentation with text classification methods.
- Research into low-resource language NLP.
- Demonstrations of data annotation and evaluation workflows.

The dataset is experimental and should not be treated as a validated benchmark or used for high-stakes decisions.

## 11. Known limitations and risks

1. **Source dependence:** All records derive from Sindhi source material. Their relationship to the original source requires continued documentation.
2. **Linguistic validation:** The dataset has not undergone comprehensive validation by a broad group of proficient Dholuo speakers.
3. **Dialect coverage:** The dataset does not establish broad representation across Dholuo varieties.
4. **Label uncertainty:** Some sentiment labels may require further assessment by proficient speakers.
5. **Small dataset size:** A 300-record dataset is insufficient to establish broad real-world generalisation.
6. **Sentiment ambiguity:** Sarcasm, idioms, context, spelling variation and mixed sentiment can affect classification.
7. **Review coverage:** Although all 60 test records were independently reviewed, only 83 records were independently reviewed overall.
8. **Source rights:** The original source listing identifies a CC BY-NC 4.0 licence. The applicable attribution, derivative-data and redistribution terms still require confirmation.

## 12. Ethical and licensing considerations

The original source is attributed to Ali Nawaz and listed on Mozilla Data Collective:

https://mozilladatacollective.com/datasets/cmrlqkecf00jynu07k7fb90iv

The source listing identifies a CC BY-NC 4.0 licence. The team must confirm the applicable licence conditions, attribution requirements and whether the proposed publication or redistribution of the Dholuo-derived contribution is permitted.

Recorded contributor permissions do not automatically resolve upstream source-data rights.

The dataset should not be publicly redistributed until the applicable rights and permissions have been reviewed.

Contributor and reviewer identities should be handled responsibly. Codes are used in the dataset metadata rather than publishing personal details.

## 13. Maintenance and versioning

The dataset should be versioned whenever records, labels, provenance information or review metadata change.

Each submitted version should be accompanied by:

- A dataset version identifier.
- A record and label count.
- A split distribution.
- A duplicate and quality audit.
- A review-status summary.
- Source and licence information.
- A record of material corrections.

**Current status:** The final 300-record contribution dataset has passed structural validation and duplicate checks. Independent review covers all test records and 83 records overall. Broader Dholuo linguistic validation and source-data redistribution review remain limitations requiring further work.
