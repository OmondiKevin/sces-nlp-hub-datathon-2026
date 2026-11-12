
from pathlib import Path

import joblib
import streamlit as st

from core import FRIENDLY, extract


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LuoSense | Dholuo sentiment",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1120px;
            padding-top: 2.2rem;
            padding-bottom: 3.5rem;
        }

        .hero {
            padding: 1.5rem 1.7rem;
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 18px;
            background: linear-gradient(
                120deg,
                rgba(16, 185, 129, 0.11),
                rgba(59, 130, 246, 0.07)
            );
            margin-bottom: 1.4rem;
        }

        .eyebrow {
            color: #10a37f;
            font-size: 0.76rem;
            font-weight: 750;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .main-heading {
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.12;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .subheading {
            color: #8b949e;
            font-size: 1.02rem;
            line-height: 1.6;
            max-width: 760px;
            margin-bottom: 0.2rem;
        }

        .result-card {
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-left: 5px solid #0d9488;
            background: rgba(13, 148, 136, 0.08);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .result-card.positive {
            border-left-color: #16a34a;
            background: rgba(22, 163, 74, 0.09);
        }
        .result-card.negative {
            border-left-color: #dc5252;
            background: rgba(220, 82, 82, 0.09);
        }
        .result-card.neutral {
            border-left-color: #64748b;
            background: rgba(100, 116, 139, 0.09);
        }
        .sample-intro {
            color: #8b949e;
            font-size: 0.9rem;
            margin-top: -0.35rem;
            margin-bottom: 0.7rem;
        }

        .result-label {
            font-size: 2rem;
            line-height: 1.2;
            font-weight: 800;
            margin-top: 0.35rem;
        }

        .small-note {
            color: #8b949e;
            font-size: 0.82rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        div.stButton > button[kind="primary"] {
            min-height: 3rem;
            border-radius: 10px;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            padding: 0.8rem 0.9rem;
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 12px;
            background: rgba(128, 128, 128, 0.045);
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 12px;
        }

        @media (max-width: 700px) {
            .block-container {
                padding-top: 1rem;
            }
            .hero {
                padding: 1.1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🌍 Dholuo NLP")
    st.caption("African-language NLP demonstration")

    st.divider()

    track = "sentiment"
    st.caption("Task: Sentiment analysis")

    st.divider()

    st.markdown("### About this demo")
    st.write(
        "This application demonstrates natural language "
        "processing for Dholuo text."
    )

    st.markdown("**Supported tasks**")
    st.write("- Sentiment analysis")

    st.divider()

    st.caption("Team 11 | NLP Hub Datathon 2026")


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

path = Path("artifacts") / track / "model.joblib"

st.markdown(
    '<div class="hero">'
    '<div class="eyebrow">NLP HUB DATATHON 2026 · TEAM 11</div>'
    '<div class="main-heading">LuoSense</div>'
    '<div class="subheading">'
    'A closer look at the tone of Dholuo text. '
    'Explore real sentences from our dataset or write your own to see '
    'how the model interprets them.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

if not path.exists():
    st.info(
        f"No trained model was found for **{track.capitalize()}**. "
        "Train this task first, then try again."
    )
    st.stop()

try:
    pack = joblib.load(path)
except Exception as error:
    st.error(f"Could not load the model: {error}")
    st.stop()


# --------------------------------------------------
# MODEL INFORMATION AND WARNINGS
# --------------------------------------------------

if pack.get("practice", False):
    st.warning(
        "PRACTICE MODE: This model uses constructed English "
        "teaching examples."
    )

st.markdown(
    '<div class="eyebrow" style="margin-top:-0.35rem;">DHOLUO · SENTIMENT EXPLORER</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.subheader("Explore Dholuo sentiment")

st.write(
    "Choose a sentence above, or enter your own text below."
)

# Load genuine examples from the canonical contribution dataset.
# Each card displays the sentence itself; clicking it loads that sentence
# into the input box so the visitor can run the classifier.
def load_demo_examples():
    import pandas as pd

    csv_path = Path("data") / "contribution.csv"
    if not csv_path.exists():
        return {}

    frame = pd.read_csv(csv_path)
    columns = {str(column).strip().lower(): column for column in frame.columns}

    text_column = next(
        (columns[name] for name in ("text", "sentence", "dholuo_text", "utterance")
         if name in columns),
        None
    )
    label_column = next(
        (columns[name] for name in ("label", "sentiment", "sentiment_label", "target")
         if name in columns),
        None
    )

    if text_column is None or label_column is None:
        return {}

    examples = {}
    for _, row in frame.iterrows():
        label_value = str(row[label_column]).strip().lower()
        sentence = str(row[text_column]).strip()
        if (
            label_value in ("positive", "negative", "neutral")
            and sentence
            and sentence.lower() != "nan"
        ):
            examples.setdefault(label_value, sentence)

    return examples


demo_examples = load_demo_examples()

if demo_examples:
    st.markdown("### Start with a real sentence")
    st.markdown(
        '<div class="sample-intro">These examples are taken directly from the submitted dataset. '
        'Choose a sentence to place it in the analyser, then select Analyse.</div>',
        unsafe_allow_html=True
    )

    sample_columns = st.columns(3)
    sample_details = [
        ("positive", "Example 01", "✦"),
        ("negative", "Example 02", "✦"),
        ("neutral", "Example 03", "✦"),
    ]

    for column, (sample_key, sample_title, sample_icon) in zip(sample_columns, sample_details):
        with column:
            with st.container(border=True):
                if sample_key in demo_examples:
                    st.caption(f"{sample_icon} {sample_title}")
                    st.markdown(f"_{demo_examples[sample_key]}_")
                    st.button(
                        "Use this sentence",
                        key=f"load_{sample_key}_example",
                        use_container_width=True,
                        on_click=lambda value=demo_examples[sample_key]: st.session_state.update(
                            {"user_text": value}
                        )
                    )
                else:
                    st.caption(sample_title)
                    st.write("No example available.")
                    st.button(
                        "Example unavailable",
                        key=f"missing_{sample_key}",
                        disabled=True,
                        use_container_width=True
                    )


user_text = st.text_area(
    "Enter a Dholuo sentence",
    placeholder="Type or paste a Dholuo sentence here...",
    height=130,
    key="user_text"
)

predict_clicked = st.button(
    "Analyse sentiment",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict_clicked:

    if not user_text.strip():
        st.info("Please enter a sentence before analysing it.")

    else:
        try:
            with st.spinner("Analysing your sentence..."):

                model = pack["model"]

                label = model.predict([user_text])[0]

                probabilities = model.predict_proba([user_text])[0]

                confidence = max(probabilities)

                friendly_label = FRIENDLY.get(label, label)

            st.divider()
            st.subheader("Analysis result")
            st.markdown("**Sentence analysed**")
            st.info(user_text)

            # SENTIMENT CLASSIFICATION
            if track == "sentiment":

                st.markdown(
                    f"""
                    <div class="result-card {str(label).lower()}">
                        <div class="small-note">Predicted sentiment</div>
                        <div class="result-label">{friendly_label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(
                    "The model assigns one of its known sentiment labels "
                    "to the sentence."
                )

            # INTENT CLASSIFICATION
            elif track == "intent":

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="small-note">Predicted intent</div>
                        <div class="result-label">{friendly_label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.info(
                    "Simulated route only. No calendar, music, weather "
                    "or other external action has been executed."
                )

            # SEMANTIC PARSING
            elif track == "semantic":


                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="small-note">Predicted intent</div>
                        <div class="result-label">{friendly_label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                slots = extract(user_text, pack["slot_memory"])

                st.markdown("### Extracted information")

                st.json({
                    "intent": label,
                    "slots": slots
                })

                st.caption(
                    "Training-only surface-value matcher: unseen slot "
                    "values may be missed. No date/time normalisation "
                    "or real action is performed."
                )

            # PROBABILITY BREAKDOWN
            st.markdown("### Class probability breakdown")

            # Match probabilities to their actual class labels
            classes = model.classes_

            probability_data = sorted(
                zip(classes, probabilities),
                key=lambda item: item[1],
                reverse=True
            )

            for class_label, probability in probability_data:
                friendly_class = FRIENDLY.get(class_label, class_label)

                st.write(f"**{friendly_class} — {probability:.1%}**")
                st.progress(float(probability))

            st.caption(
                "These probabilities represent the model's estimated scores "
                "for each available class. They are uncalibrated and should "
                "not be interpreted as guaranteed correctness."
            )

            # SENTIMENT-SPECIFIC LIMITATION
            if track == "sentiment":
                st.info(
                    "This is sentence-level opinion classification. "
                    "It is not emotion detection, sarcasm understanding "
                    "or a diagnosis."
                )

        except Exception as error:
            st.error(f"An error occurred during prediction: {error}")


# --------------------------------------------------
# ABOUT THE MODEL
# --------------------------------------------------

st.divider()


with st.expander("About the model and methodology"):

    st.markdown("### Dataset")

    st.metric("Dataset records", "300")

    st.write(
        "The final Dholuo sentiment dataset contains "
        "300 records, balanced across three sentiment classes."
    )

    dataset_col1, dataset_col2, dataset_col3 = st.columns(3)

    dataset_col1.metric("Positive", "100")
    dataset_col2.metric("Negative", "100")
    dataset_col3.metric("Neutral", "100")

    st.caption(
        "All 300 records are derived from Sindhi source material. "
        "Google Translate produced the initial Dholuo drafts for all 300 records. "
        "Of these, 276 were used largely as translated (machine_translated) and 24 were subsequently human-localised (human_localised)."
        " The dataset is split into 180 training, 60 development "
        "and 60 test records."
    )

    st.caption(
        "Review metadata: 217 self-reviewed records and 83 "
        "independently reviewed records. All 60 test records are "
        "marked independently reviewed in the supplied metadata."
    )

    st.markdown("### Model methodology")

    st.write(
        "**Feature extraction:** Character-level TF-IDF "
        "using 2–5 character n-grams."
    )

    st.write(
        "**Classification algorithm:** Logistic Regression "
        "with a maximum of 1,000 iterations."
    )

    st.write(
        "**Evaluation approach:** Training and development data "
        "were used for model fitting and development evaluation. "
        "The held-out test set was evaluated separately after "
        "the model was frozen."
    )

    st.markdown("### Final test evaluation")

    metric_col1, metric_col2 = st.columns(2)

    metric_col1.metric("Test accuracy", "61.67%")
    metric_col2.metric("Test macro-F1", "0.6111")

    st.caption(
        "Evaluation on 60 held-out test records. These results "
        "are specific to this dataset and should be interpreted "
        "with its size and language-quality limitations in mind."
    )

    st.markdown("### Development evaluation")

    st.write(
        "**Development accuracy:** 70.00%"
    )

    st.write(
        "**Development macro-F1:** 0.6984"
    )

    st.markdown("### Known limitations")

    st.write(
        "- The dataset is relatively small, with 300 records."
    )

    st.write(
        "- Independent review covers 83 records overall. All 60 "
        "held-out test records were independently reviewed; the "
        "remaining records have varying review status."
    )

    st.write(
        "- The model may struggle with dialect differences, "
        "sarcasm, mixed-language text and unfamiliar expressions."
    )

    st.write(
        "- Predictions are estimates and may not reflect the "
        "intended meaning of every Dholuo sentence."
    )

    st.warning(
        "This is a research demonstration, not a production-ready "
        "language system. Evaluation results should not be treated "
        "as proof of general performance across Dholuo speakers "
        "or dialects."
    )



# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "NLP Hub Datathon 2026 | Team 11 | Dholuo Sentiment Analysis"
)

st.caption(
    "Experimental research demonstration. Results should be "
    "interpreted with the model's data and evaluation limitations in mind."
)
