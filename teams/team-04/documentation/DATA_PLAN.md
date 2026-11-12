# Data plan
* **Team / task / primary language / variety:** Team 4 (SautiByte) / Track A (Intent Classification) / Kiswahili / Kenyan conversational variety.
* **Reviewer and capacity (keep private contact details separate):** Brian, Leo, and Zakariya acting in a round-robin independent review capacity. All are fluent speakers.
* **Chosen dataset URL/version or permitted authored-data plan:** Permitted authored-data plan (`team_authored`).
* **Contribution type and record target:** 250 newly authored text records (25 per intent).
* **Labels and edge cases:** 10 MASSIVE labels. Edge cases involving multi-intent requests or ambiguous sentiment were explicitly excluded.
* **Train/dev/test grouping and independent review:** 15 train / 5 dev / 5 test per label. Close paraphrases generated during drafting share a `group_id` and are kept in the exact same split to prevent data leakage. Test records are strictly reviewed by a non-authoring member.
* **Who does data / review / code / documentation:**
  * Data/Review: Shared evenly among Brian, Leo, and Zakariya.
  * Code/Demo: Zakariya and Leo.
  * Documentation: Brian.
* **Access/compute risks and help needed:** Local machine compute (Python 3.10 virtual environment) is sufficient for the TF-IDF logistic regression baseline.
* **Organiser confirmation and date:** 10 November 2026.[cite: 56, 61]