# Contributions and AI use

Team 14 (Maa) | Strathmore NLP Hub Datathon 2026

## Member contributions

We split the work by assigning GitHub issues. Where an AI tool did part of the work, the AI section below says so.

| Member | Data / technical / documentation / review contribution | Evidence |
|---|---|---|
| Philip Tait | Made the Google Form and collected the responses. Added the starter kit, wrote the data plan, wrote this statement, and froze and submitted the project. Also set up the repo, issues, milestones and board, and approved pull requests. | Issues #1, #2, #4, #16, #18. PRs #19 and #20 |
| Neema Mapelu Naserian | Wrote the annotation guide. Did the cleaning, groups and splits. Worked with the reviewer (R01) and logged the review. Built `data/contribution.csv`. Wrote the dataset card and quality report. | Issues #3, #5, #6, #7, #8, #14, #15. PRs #21 to #27 |
| Mayabi Muigai Ivan | Trained the baseline, ran the final evaluation, did the error analysis, built the Streamlit demo, recorded the demo and wrote the README. | Issues #9, #10, #11, #12, #13, #17. PRs #29 to #33 |

R01 is an outside native Maa speaker who reviewed all the raw answers. R01 is not on the team, and is a relative of a team member (see `docs/review_log.md`).

## Upstream datasets/code reused and attribution

- The organiser starter kit v2.0. The code is MIT and the practice data is CC0. The practice CSVs count as zero contribution records.
- MASSIVE, for the label names only. We did not use any rows from it.

## AI tools used, dates, purpose and affected records/files

**Neema: Claude Code (Anthropic), 5 to 11 November 2026**
- Wrote a Windows run guide for the starter kit.
- Searched for existing Maa datasets and found none.
- Counted what R01 changed by comparing the raw and reviewed files: 136 answers deleted, 124 corrected, 0 label changes. The review decisions were R01's.
- Wrote `clean_responses.py`. It normalised the text, removed 68 duplicates, made the contributor codes (C01 to C41), made the group IDs and made the seeded train/dev/test split. The script stays outside the repo because it handles Maa text.
- Suggested 19 more exclusions: 4 non-Maa answers, 8 single words that could fit several intents, 5 noun phrases with no request, and 2 list sentences asking what is on the list. We accepted them. They were based on sentence structure, not on knowing Maa, and are logged privately in `dropped_rows.csv`.
- Set `reviewer_code` to R01 and `review_status` to `independently_reviewed` on all 1,024 records, after Neema confirmed R01 had checked every answer.
- Files affected: `data/contribution.csv`, `docs/`, and the contents of PRs #21 to #27.

**Ivan: Gemini and Claude (dates not recorded)**
Used while building the Streamlit demo and writing the README. 
- Ran the baseline once on the cleaned file as a sanity check, before the official run. 
- Listed the 15 test errors and drafted the error analysis and project documents from our real numbers. The English glosses of Maa words in the error analysis are rough and no Maa speaker has checked them.

  
**Philip: Claude (claude.ai), 9 to 12 November 2026, and Claude Code, 12 November 2026**
Claude helped with planning, GitHub guides for the team, the form structure and situation prompts, packaging the starter kit and drafting some documents. Claude Code was used on 12 November to check the repo against the submission checklist, and Philip made the fixes himself. Files affected: documentation drafts, the starter-kit package and `docs/`.

None of these tools wrote, translated, corrected or labelled any Maa text.

## Human checks applied

- Every Maa answer was written by a human contributor through the form. R01, a native Maa speaker, checked all the raw answers.
- Philip approved pull requests before they were merged.
- The numbers in the README and the documents come from the saved files in `artifacts/intent/` and `data/contribution.csv`.

## Any generated suggestions rejected

We did not use these AI-made items for the final data: a form-building script and converter (our real form had a different layout), and a reviewer sheet and cleaning script (`build_candidates.py`) from Philip's Claude session. We did not keep a record of any other suggestions we turned down.

No AI-generated text or labels counted as independently validated human data.
