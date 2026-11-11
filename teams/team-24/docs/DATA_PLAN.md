# Data plan — Team 24 (Kiswahili 5)

Version: 2026-11-11 (final-stage record of what was actually done). 

**Team / task / language / variety**
- Team 24, "Kiswahili 5". Members: Moses (code 24M), Krysia (24K), Nathan (24N).
- Task: **Track A, intent classification**, 10 MASSIVE-aligned labels (see `taxonomy.csv`).
- Language: Kiswahili, locale tag `sw-KE`. Variety: everyday Kenyan Swahili in a spoken-request register, including some informal forms (e.g. *Naeza*, *Nikona*, *ama*). A few rows keep the English loanword *alarm* (24-054, 24-060, 24-071) because it is genuinely used; other rows use *kengele*.

**Reviewer and capacity**
- Moses (24M) reviewed 43 of the 52 test rows and the train/dev rows (see QUALITY.md). Nathan (24N) reviewed the other 9 test rows. All reviewers state they are fluent in Kiswahili.

**Source plan and what was actually used**
- Planned route: Route B, human-authored examples written from everyday situations.
- Final contribution: **262 rows, all `original_human` / `team_authored`.**
- An initial batch of 110 rows copied from the GitHub repo `Rogendo/Eng-Swa-Dataset` (`swa.txt`) was **excluded**: the repo has no licence (GitHub API `license: null`), no stated provenance, and its rows did not fit the intents. See DATA_CARD.md.
- MASSIVE and Common Voice were not used for the contribution.

**Contribution type and target**
- Target: at least 250 rows, per label at least 15 train / 5 dev / 5 test. Achieved: 262 rows (159 train / 51 dev / 52 test); every label meets the minimum.

**Labels and edge cases**
- See ANNOTATION_GUIDE.md. Main edge cases: set vs query (calendar, lists), alarm vs timer vs reminder, definition vs general factual question, news vs factual question, and requests the 10 labels do not cover (removing items, stopping music, search).

**Train / dev / test grouping and independent review**
- Each row has its own `group_id` (no shared sources or paraphrases). Splits are stratified by label by hand.
- All test rows were checked by someone other than their recorded author.

**Who does data / review / code / documentation**
- Data: Krysia and Nathan (authorship per the contribution file; see CONTRIBUTIONS.md). Review: Moses, Nathan. Code, validation and documentation drafting: Moses with AI assistance (declared in CONTRIBUTIONS.md). 

**Access / compute risks**
- None blocking. CPU-only baseline. Model files are not committed (`*.joblib` is git-ignored); they are rebuilt with `train.py`.

