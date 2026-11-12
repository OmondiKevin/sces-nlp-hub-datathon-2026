# Data plan — Team 19

**Team:** 19 (Harry Sigei, Ezra Ntwiga, Michael Majau)
**Task:** Track A, intent classification (10 MASSIVE-aligned action labels in `taxonomy.csv`)
**Primary language / variety:** Kiswahili (`sw-KE`); regional variety and spelling conventions: **[confirm with the writers and reviewer]**. The team requested to change its language from Kalenjin, and the organiser approved proceeding with Kiswahili by WhatsApp on 7 Nov 2026. Keep the screenshot/private organiser correspondence out of public GitHub; record the approval in the team's private evidence.

**Reviewer and capacity:** A competent Kiswahili reviewer from outside the team is required. Confirm that `T19-R1` is qualified to review the selected Kiswahili variety and available to independently review every test record plus a sample of training records. Keep contact details and permission evidence private. The earlier reviewer/dialect assumption for Kalenjin is not confirmation of Kiswahili review capacity.

**Source:** Use Route B: new examples written by people competent in the selected Kiswahili variety (`source_method = original_human`, `source_dataset = team_authored`). Do not count downloaded, machine-translated or AI-generated sentences as original human contributions. Obtain and document permission for the intended use.

**Contribution target:** 250 accepted records, 25 per label (15 train, 5 dev, 5 test). Stretch goal only if time allows and quality holds.

**Labels and edge cases:** We use the 10 labels and boundary rules in `taxonomy.csv`. Key edge cases: weather forecast (`weather_query`) vs. news about weather (`news_query`); alarm (`alarm_set`) vs. calendar event (`calendar_set`); creating vs. reading a calendar or list. Natural Kiswahili–English code-switching is kept and recorded, not treated as an error. Spelling conventions are agreed with the reviewer and recorded in the annotation guide.

**Splits and review:** Each unrelated record gets its own `group_id`; paraphrases or related examples share a `group_id` and stay in one split. Every test record must be independently reviewed by a competent Kiswahili reviewer who did not author it. Use `T19-R1` only if their qualifications and availability are confirmed. Disagreements and exclusions are logged in the quality report.

**Roles:**
- Harry Sigei (`T19-A`): data lead; confirm Kiswahili writing/review capability before assigning language-quality decisions; model training, evaluation and demo.
- Ezra Ntwiga: **[e.g. documentation: dataset card, quality report, source log]**
- Michael Majau: **[e.g. GitHub repository, README, demo recording]**

**Risks / help needed:** Confirm the Kiswahili variety, spelling conventions, and competent independent reviewer. One main writer limits stylistic variety (we plan to vary situations, sentence length and phrasing deliberately). The organiser's WhatsApp approval permits proceeding with Kiswahili; it does not by itself confirm reviewer capacity or change the task from intent classification to translation.

**Organiser confirmation and date:** Kiswahili language change approved by WhatsApp on 7 Nov 2026. The organiser's reply to Team 12 says the provided labels can be used and labels may be extended based on MASSIVE; confirm at the final review whether adding a translation intent changes the agreed scope, schema, or required evaluation.
