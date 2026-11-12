# Source Log — Team 6: Data Buddies

## 1. Purpose and privacy

This document records the sources, provenance, permissions, and corrections associated with the Team 6 Luganda Intent Corpus.

The public repository intentionally contains no private permission evidence, personal details, or source files that have not been cleared for publication. Written consent records are held in the team's private storage and are referenced by source group in this document.

All 250 accepted utterances were originally authored by a team contributor. No downloaded MASSIVE utterances or other external dataset records are included in `data/contribution.csv`.

## 2. Sources by record group

| Record ID group | Source method | Source dataset | Version | Licence/permission | Private evidence location |
|---|---|---|---|---|---|
| `LG-WEA-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-DAT-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-ALA-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-CAL-*` — `calendar_set` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-CAL-*_2` — `calendar_query` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-LIS-*` — `lists_createoradd` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-LIS-*_2` — `lists_query` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-PLA-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-NEW-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |
| `LG-QA-*` | `original_human` | `team_authored` | `v1` | `documented_contributor_permission` | Team private storage |

**Contributor:** `T06-A` — Poni Yokwe  
**Reviewer:** `REV-LG-2026` — external fluent Luganda reviewer who did not author the reviewed records.

The `_2` suffix identifies records whose IDs were changed to resolve duplicates; it does not represent a different source or dataset version.

## 3. Corrections log

During validation, 50 duplicate `record_id` values were identified. The duplicates occurred because the original ID namespaces were reused across paired intent categories, including the calendar and list intents.

The duplicate IDs were resolved using `fix_ids.py`. The second occurrence of each duplicated ID received the suffix `_2`. The original text and intent labels were not changed, and the original `evidence/REVIEW_LOG.csv` was retained as provenance evidence.

| Record ID | Field | Original value | Corrected value | Reason | Reviewer | Date |
|---|---|---|---|---|---|---|
| `LG-LIS-024` (second occurrence) | `record_id` | `LG-LIS-024` | `LG-LIS-024_2` | Duplicate ID caused by a reused namespace. Text and label remained unchanged. | `REV-LG-2026` confirmed text and label | 2026-11-11 |

**Correction summary:** All 50 duplicate ID occurrences were resolved by `fix_ids.py` by assigning `_2` suffixes to the second occurrences. No text or label changes were made as part of this correction.

## 4. Upstream resources and credit

The project acknowledges the following resources:

- **Starter kit v2.0:** Used as the project starter structure and validation framework. Refer to the starter kit README for its licence and attribution requirements.
- **MASSIVE label schema:** Used as the reference for the ten intent label names. The project uses the label schema only; no MASSIVE dataset utterances are included in the team's contribution.  

No MASSIVE, Common Voice, AfriSenti, or KINNEWS records are included in `data/contribution.csv`.

## 5. Permission and evidence handling

The dataset records use the permission value `documented_contributor_permission`. Written consent evidence is held in the team's private storage and is not included in the public repository.

The public repository therefore provides provenance references without exposing private consent records or personal information. The team should retain access to the private evidence in case permission needs to be verified during project review.