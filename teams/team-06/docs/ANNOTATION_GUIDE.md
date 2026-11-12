# Annotation Guide — Luganda Intent Classification (Track A)

## 1. Purpose

This guide defines the annotation rules used to classify Luganda utterances into the ten MASSIVE-aligned intent categories selected for Team 6's Track A project.

It establishes consistent labelling boundaries, provides real examples from the contributed dataset and documents the language-handling and independent review procedures followed during annotation.

The objective is to ensure that each utterance is assigned an appropriate intent label based on its meaning and intended action.

## 2. General Annotation Rules

The following rules were applied throughout the annotation process:

1. **One Intent per Record:** Each utterance must express one clear and identifiable intent.
2. **Meaning-Based Classification:** Labels are assigned according to the user's intended meaning rather than individual keywords.
3. **No Forced Labels:** Unclear, unsupported or multi-intent examples are excluded rather than assigned an unsuitable label.
4. **Exclusion Documentation:**  Any excluded example must be documented in QUALITY.md with the reason. (In this dataset, no records were excluded — see QUALITY.md).
5. **Consistent Label Boundaries:** Similar requests must be classified consistently according to the definitions and distinctions in this guide.

## 3. Intent Labels and Examples

The following table defines the ten intent categories and provides examples taken directly from `data/contribution.csv`.

| Intent Label | When to Use | Luganda Example |
|---|---|---|
| `weather_query` | Requests for current weather conditions or weather forecasts. | `Embeera y'obudde eritya leero?` |
| `datetime_query` | Requests for the current time, date or day. | `Ssaawe zimeka mu kaseera kano?` |
| `alarm_set` | Requests to create an alarm that rings at a specified time. | `Teegeka alamu ya ssaawe kkumi n'emuu n'akitundu ez'emakya nkya.` |
| `calendar_set` | Requests to create a calendar event or scheduled reminder. | `Yongera okulabagana n'omusawo mu kalenda ku Lwakubiri ssaawe nnya ez'emakya.` |
| `calendar_query` | Requests to retrieve or read existing calendar events. | `Biki ebiri ku kalenda yange leero?` |
| `lists_createoradd` | Requests to create a new list or add an item to an existing list. | `Kola olukalala lw'ebintu eby'okugula mu katale.` |
| `lists_query` | Requests to retrieve or read the contents of an existing list. | `Biki ebiri ku lukalala lw'ebintu eby'okugula?` |
| `play_music` | Requests to start playing music or a specific song. | `Zannya oluyimba lwa 'Sitya Loss'.` |
| `news_query` | Requests to retrieve or read news articles and headlines. | `Mbuulira amawulire ag'amangu amapya leero.` |
| `qa_definition` | Requests for the meaning or definition of a word or concept. | `Komyuta kiki mu bufunze?` |

## 4. Label Boundary Decisions

The following distinctions were established to prevent confusion between similar intent categories.

### 4.1 Weather Queries vs. News Queries

- `weather_query`: Used when the user requests weather conditions or a forecast.
- `news_query`: Used when the user requests news coverage or headlines, including news about weather events.

**Examples:**
- Requesting tomorrow's weather forecast → `weather_query`
- Asking to read news about a storm → `news_query`

### 4.2 Date and Time Queries vs. Alarm Setting

- `datetime_query`: Used when the user asks for the current time, date or day.
- `alarm_set`: Used when the user wants an alarm configured for a particular time.

**Examples:**
- `Ssaawe zimeka mu kaseera kano?` → `datetime_query`
- Requesting an alarm for a wake-up time → `alarm_set`

### 4.3 Calendar Creation vs. Calendar Retrieval

- `calendar_set`: Used when the user wants to create or schedule an event or reminder.
- `calendar_query`: Used when the user wants to view existing calendar events.

### 4.4 List Creation vs. List Retrieval

- `lists_createoradd`: Used when the user wants to create a list or add an item to one.
- `lists_query`: Used when the user wants to view the contents of an existing list.

### 4.5 Music Playback vs. Factual Music Questions

- `play_music`: Used when the user explicitly requests music playback.
- A factual question about a song, artist or music-related topic is not classified as `play_music`.

### 4.6 Definition Requests vs. General Questions

- `qa_definition`: Reserved for requests asking for the meaning or definition of a word or concept.
- General factual questions that do not request a definition are outside this category and should be excluded rather than forced into this label.

## 5. Language Handling Guidelines

The following language-handling principles were followed during dataset authorship and review.

### 5.1 Natural Luganda Expressions

Utterances were written in natural Luganda using the provided English meaning prompts as guidance.

The author was not required to produce direct, word-for-word translations. Instead, the focus was on expressing the intended meaning naturally in Luganda.

### 5.2 Spelling and Apostrophe Preservation

Original spelling and apostrophe usage were preserved in the contributed records.

Examples include:

- `y'obudde`
- `lw'ebintu`
- `ez'emakya`

No additional text normalisation was applied to these forms.

### 5.3 Code-Switching

Genuine code-switching was retained where it occurred naturally in the language.

Code-switching was not automatically treated as a linguistic error.

### 5.4 Personal and Sensitive Information

No personal or sensitive details were included in the request texts.

## 6. Independent Review Protocol

All contributed records underwent independent review by `REV-LG-2026`, an external fluent Luganda speaker who was not an author of the records being reviewed.

### 6.1 Review Coverage

- All 250 contributed utterances were submitted for independent review.
- Every reviewed record is marked `independently_reviewed`.
- All 50 testing records, representing five examples per intent, were independently reviewed.

### 6.2 Review Criteria

Each record was assessed using three main criteria:

| Review Criterion | What Was Checked |
|---|---|
| Linguistic Naturalness | Whether the Luganda utterance reads naturally and communicates the intended meaning. |
| Intent-Label Suitability | Whether the assigned intent label correctly represents the user's intended action according to the boundary rules in this guide. |
| Meaning Preservation | Whether the Luganda utterance accurately expresses the intended meaning provided by the English prompt. |

### 6.3 Review Evidence

Individual review decisions and disagreements were recorded in:

`../evidence/REVIEW_LOG.csv`

The overall findings and quality assessment are documented in:

`QUALITY.md`

## 7. Automated Validation and Human Review

Automated validation and human review served different purposes in the dataset quality assurance process.

### 7.1 Automated Validation

The `validate.py` script checks structural requirements, including:

- Required dataset columns and structure.
- Dataset split sizes.
- Record ID uniqueness.

The final contribution dataset returned:

**`PASS: 250 records`**

### 7.2 Limitations of Automated Validation

Passing automated validation does not establish that:

- The Luganda utterances are linguistically natural.
- The assigned intent labels are semantically correct.
- The utterances preserve the intended meaning of their English prompts.
- Contributor permissions are genuine or properly documented.

These aspects require human assessment and supporting evidence.

### 7.3 Human Quality Assurance

Linguistic naturalness, label suitability, meaning preservation and data permissions were assessed separately.

The relevant evidence and findings are documented in:

- `QUALITY.md` — dataset quality and independent review findings.
- `SOURCE_LOG.md` — data provenance and contributor permission documentation.

## 8. Annotation Consistency

All annotations were guided by the same ten intent definitions and boundary decisions documented in this guide.

The one-intent-per-record rule, exclusion of unsupported examples and independent review process were used to promote consistency throughout dataset preparation.

This guide serves as the reference for interpreting the contributed labels and understanding the annotation decisions made by the team.

---

**Team 6 — Data Buddies**  
*Luganda Intent Classification | Track A*