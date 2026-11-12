# Data Quality Report – Team 11 Dholuo Sentiment Dataset

**Team:** Team 11 – NLP Hub Datathon 2026  
**Language:** Dholuo  
**Task:** Three-class sentiment classification  
**Report version:** Final contribution audit v1.0  
**Date:** 11 November 2026  
**Status:** Structural validation completed; linguistic and source-rights limitations remain

## 1. Purpose

This report documents the checks performed on the final 300-record Dholuo sentiment contribution dataset.

It records dataset composition, duplicate checks, split integrity, review coverage, metadata and official validator results.

Structural validation is distinguished from linguistic quality assessment and source-rights verification. Passing automated checks does not establish that every sentence is natural Dholuo, that every sentiment label is correct or that redistribution is authorised.

## 2. Dataset examined

The final contribution dataset used for training and evaluation is:

`data/contribution.csv`

The source workbook used to prepare the final contribution is:

`Team_11_Dholuo_Sentiment_Dataset_Final.xlsx`

The dataset contains 15 fields covering text, sentiment labels, source information, contribution metadata, review status, grouping and dataset split.

The original source material is attributed to Ali Nawaz and listed on Mozilla Data Collective:

- Dataset title: Sindhi Sentiment Analysis Dataset
- Steward: Ali Nawaz
- Dataset ID: `cmrlqkecf00jynu07k7fb90iv`
- Source URL: https://mozilladatacollective.com/datasets/cmrlqkecf00jynu07k7fb90iv
- Listed licence: CC BY-NC 4.0

All 300 Dholuo records derive from Sindhi source material. Google Translate was used to produce the initial Dholuo drafts for all records. The recorded contribution methods are:

- 276 `machine_translated` records: Google Translate output used largely as produced.
- 24 `human_localised` records: initial Google Translate drafts subsequently human-localised.

The relationship to the upstream source remains relevant to provenance and licensing review.

## 3. Final dataset composition

### Label distribution

| Label | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| **Total** | **300** |

### Split distribution

| Split | Records |
|---|---:|
| Training | 180 |
| Development | 60 |
| Test | 60 |
| **Total** | **300** |

The per-label distribution is:

| Label | Train | Development | Test | Total |
|---|---:|---:|---:|---:|
| Positive | 60 | 20 | 20 | 100 |
| Negative | 60 | 20 | 20 | 100 |
| Neutral | 60 | 20 | 20 | 100 |
| **Total** | **180** | **60** | **60** | **300** |

## 4. Duplicate and structural audit

The final contribution CSV was checked using normalised text comparisons and metadata checks.

| Measure | Final finding |
|---|---:|
| Total records | 300 |
| Unique record IDs | 300 |
| Unique normalised texts | 300 |
| Duplicate record IDs | 0 |
| Duplicate normalised texts | 0 |
| Missing required values | 0 |
| Group IDs spanning multiple splits | 0 |

Normalisation used Unicode NFC, whitespace collapsing and case-folding.

No duplicate normalised text entries or cross-split group leakage were found in the final contribution dataset.

These results apply to the final contribution CSV. Earlier exploratory audits of a different working dataset produced different figures and should not be presented as the final dataset's quality results.

## 5. Review coverage

The final dataset's review metadata records:

| Review status | Records |
|---|---:|
| Self-reviewed | 217 |
| Independently reviewed | 83 |
| **Total** | **300** |

All 60 held-out test records were independently reviewed. Each test record has a reviewer code different from its contributor code.

The remaining records have varying review status. Therefore, independent review must not be claimed for all 300 records.

Independent review metadata is evidence of a separate review process, but it does not establish comprehensive agreement among fluent Dholuo speakers or broad linguistic validation.

## 6. Language quality and contextual assessment

Google Translate was used to produce the initial Dholuo drafts for all 300 records from Sindhi source material. The contribution methods recorded in the dataset are:

| Method | Records |
|---|---:|
| `machine_translated` | 276 |
| `human_localised` | 24 |
| **Total** | **300** |

The team should continue to assess:

- Naturalness and grammatical correctness.
- Idiomatic expressions and culturally appropriate phrasing.
- Negation and sentiment polarity.
- Ambiguous or mixed sentiment.
- Sarcasm and irony.
- Dialect variation and spelling differences.
- Contextual references inherited from the source material.

The available structural checks cannot determine whether every Dholuo sentence is fluent or semantically faithful. Broader assessment by proficient Dholuo speakers remains necessary.

## 7. Metadata and provenance checks

The final dataset contains fields for source, source version, source record ID, source URL, contribution method, permission, contributor, reviewer, review status, group and split.

The recorded metadata distinguishes the two human contribution methods and records review coverage.

However, the following issues remain important:

1. The exact upstream source version and record-level traceability require confirmation.
2. The source licence and its application to the Dholuo-derived contribution require review.
3. Recorded contributor permissions do not independently resolve upstream source rights.
4. Reviewer codes document review metadata but do not establish broad linguistic expertise.

No source record identifiers or rights clearances should be inferred where supporting evidence is unavailable.

## 8. Official validator

The final dataset was checked using:

```powershell
python validate.py --data data/contribution.csv --track sentiment
```

The validator returned:

```text
PASS: 300 records; language quality, permission and semantic duplicate review remain human responsibilities.
```

This confirms that the dataset passed the validator's implemented checks.

The validator explicitly leaves language quality, permission and semantic duplicate review as human responsibilities. Its successful result must not be interpreted as certification of linguistic quality or legal permission.

## 9. Final validation summary

| Validation measure | Final result |
|---|---|
| Total records | 300 |
| Positive records | 100 |
| Negative records | 100 |
| Neutral records | 100 |
| Training records | 180 |
| Development records | 60 |
| Test records | 60 |
| Unique record IDs | 300 |
| Unique normalised texts | 300 |
| Duplicate normalised texts | 0 |
| Missing required values | 0 |
| Cross-split group leakage | None detected |
| Independently reviewed records overall | 83 |
| Independently reviewed test records | 60 of 60 |
| Official sentiment validator | PASS |

### Remaining limitations

- Broader linguistic validation by proficient Dholuo speakers remains necessary.
- Dialect and code-switching coverage has not been systematically established.
- Source-version and record-level provenance require further confirmation.
- Upstream derivative-data and redistribution rights require review.

## 10. Conclusion

The final 300-record contribution dataset passed the documented structural checks, including required-field checks, duplicate checks, split-integrity checks and the official sentiment validator.

All 60 held-out test records were independently reviewed, while 83 records were independently reviewed overall.

These results represent a completed structural audit, not comprehensive linguistic validation or legal clearance for redistribution. The dataset remains experimental and its limitations must accompany any presentation or release.

**Report status:** Final structural audit documented; linguistic validation and source-rights review remain outstanding.
