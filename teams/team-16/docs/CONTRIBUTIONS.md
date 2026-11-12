# Contributions and AI use

| Member | Contribution recorded or evidenced | Evidence / status |
|---|---|---|
| Abelle Emmanuel (`contributor_001`) | The data plan assigns data collection, code, and documentation. The CSV attributes 199 `human_localised` rows to this contributor. | `templates/DATA_PLAN.md`; `data/contribution.csv`; model and documentation files in the repository.  |
| Innocent Mukiza (`contributor_002`, `reviewer_001`) | The plan names him as a native Kinyarwanda speaker, data contributor, and reviewer. The user supplied his review of five model-confusing examples. | `templates/DATA_PLAN.md`; feedback adjudicated for `kin-015`, `kin-155`, `kin-314`, `kin-319`, and `kin-327`.  |
| Atta Wasike | Team Member | `README`; |
| Amana Achieng Okello | Team Member | `README`; |

## Upstream data and code

- No row in `data/contribution.csv` identifies an external dataset: its `source_dataset` value is `original` for all 345 records.
- The organizer confirmed on 10 November 2026 that AfriSenti's Kinyarwanda subset may be used for sentiment analysis. It is not identified as a source for any row in the contribution file. The separate `data/other.csv` and `data/other2.csv` files have no source, version, or licence note alongside them; identify them and record attribution before using or counting them.
- The organizer's reply did not settle whether external examples count toward the 300-record requirement. Do not count external rows toward that target until the organizer confirms.
- Project dependencies are listed in `requirements.txt`. No separate upstream code attribution is recorded in the files reviewed.

## AI tools

| Tool / author code | Use recorded | Records / files |
|---|---|---|
| Claude (`llm_claude`) | Synthetic Kinyarwanda examples; generated 09/11/2026 | 90 records: `kin-031`–`kin-100` and `kin-191`–`kin-210`. |
| OpenAI Codex (`llm_codex`) | Generated synthetic examples for training and assisted with project documentation. Exact row-level generation dates are not stored. | 26 records: `kin-334`–`kin-359`; documentation in `templates/`. |

AI-authored text is not human-authored data. Every row marked as `independently_reviewed` was reviewed by an independent native speaker.

## Human checks and changes

- Innocent Mukiza's five-item feedback changed the labels of `kin-015`, `kin-155`, `kin-319`, and `kin-327`, and changed both wording and label for `kin-314`.
- The reviewer considered `ku munota wa nyuma` in `kin-155` understandable but possibly calqued from English. 
- `kin-161` was changed to remove a duplicate sentence after the user identified the duplicate.
- No log of rejected examples was kept.