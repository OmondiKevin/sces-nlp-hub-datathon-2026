from datetime import datetime
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Maasai NLP - Intent Classification - Team 14",
    page_icon="🌍",
    layout="wide",
)

# ------------------------------------------------------------------------------
# Sunset Theme Custom Styling (Dark Mode Only)
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #1f1124 0%, #2c162b 50%, #3a1c28 100%) !important;
        }
        div[data-testid="stExpander"] {
            background: rgba(45, 23, 42, 0.7) !important;
            border: 1px solid rgba(255, 126, 95, 0.3) !important;
        }
        section[data-testid="stSidebar"] {
            background-color: rgba(30, 15, 29, 0.5) !important;
            border-right: 1px solid rgba(255, 126, 95, 0.2);
        }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            box-shadow: 0 3px 6px rgba(255, 126, 95, 0.3) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(90deg, #feb47b 0%, #ff7e5f 100%) !important;
            transform: translateY(-1px);
        }
    }

    div[data-testid="stHorizontalBlock"] {
        overflow-x: auto;
        white-space: nowrap;
        flex-wrap: nowrap !important;
        padding-bottom: 12px;
    }

    div[data-testid="stHorizontalBlock"] > div {
        flex: 0 0 auto !important;
        min-width: fit-content !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Maasai NLP - Intent Classification")

# Team Badge & Status Bar
st.markdown(
    "🌍 **Language:** Maasai (`mas`) | **Prototype Status:** Active v1.0 |"
    " **Dataset Version:** 2026-11"
)

# ------------------------------------------------------------------------------
# 1. Load Model Artifacts
# ------------------------------------------------------------------------------
track = "intent"
path = Path("artifacts") / track / "model.joblib"
if not path.exists():
  st.error(
      f"Model artifact not found at: {path.absolute()}. Train this task"
      " first; see NEXT_STEPS.md."
  )
  st.stop()

try:
  pack = joblib.load(path)
except Exception as e:
  st.error(f"Failed to load model joblib file: {e}")
  st.stop()

# ------------------------------------------------------------------------------
# 2. Load Dataset CSV
# ------------------------------------------------------------------------------
csv_path = Path("data/contribution.csv")
df = pd.DataFrame()

if csv_path.exists():
  try:
    df = pd.read_csv(csv_path, skipinitialspace=True)
    df.columns = df.columns.str.strip()
  except Exception as e:
    pass

# ------------------------------------------------------------------------------
# 3. Initialize Session State
# ------------------------------------------------------------------------------
if "history" not in st.session_state:
  st.session_state.history = []

# ------------------------------------------------------------------------------
# 4. Sidebar Drawer for History
# ------------------------------------------------------------------------------
with st.sidebar:
  st.header("📜 Prediction History Drawer")
  if st.button("Clear History", use_container_width=True):
    st.session_state.history = []
    st.rerun()

  st.markdown("---")
  if not st.session_state.history:
    st.info("No query history recorded yet.")
  else:
    for idx, item in enumerate(st.session_state.history):
      with st.expander(
          f"[{item['timestamp']}] {item['predicted_intent']}",
          expanded=(idx == 0),
      ):
        st.markdown(f"**Text:** `{item['text']}`")
        st.markdown(f"**Predicted:** `{item['predicted_intent']}`")
        st.markdown(f"**Confidence:** `{item['confidence']:.1%}`")

# ------------------------------------------------------------------------------
# 5. Tabs Layout
# ------------------------------------------------------------------------------
tab_predict, tab_eval, tab_dataset = st.tabs([
    "🎯 Intent Predictor",
    "📊 Evaluation & Error Analysis",
    "📋 Dataset Summary & Quality",
])

with tab_predict:
  input_mode = st.radio(
      "Input Mode",
      ["Enter Custom Text", "Select from Dataset CSV"],
  )

  text = ""
  if input_mode == "Select from Dataset CSV":
    if df.empty:
      st.warning(
          "⚠️ Dataset is empty or could not be loaded from"
          " `data/contribution.csv`."
      )
      text = st.text_area("Enter text in the model language (Fallback)")
    else:
      lang = pack.get("language", "mas")
      filtered_df = (
          df[df["language"].str.strip() == lang]
          if "language" in df.columns
          else df
      )
      if filtered_df.empty:
        filtered_df = df

      if "label" in df.columns:
        intents = sorted(filtered_df["label"].dropna().unique().tolist())

        if "selected_intent" not in st.session_state:
          st.session_state.selected_intent = intents[0] if intents else "All"

        st.markdown("**Filter by Intent:**")
        cols = st.columns(len(intents) if len(intents) > 0 else 1)
        for i, intent in enumerate(intents):
          with cols[i]:
            button_type = (
                "primary"
                if st.session_state.selected_intent == intent
                else "secondary"
            )
            if st.button(intent, key=f"intent_btn_{intent}", type=button_type):
              st.session_state.selected_intent = intent
              st.rerun()

        selected_intent = st.session_state.selected_intent
        st.caption(f"Active Intent Filter: **{selected_intent}**")

        if selected_intent and selected_intent != "All":
          filtered_df = filtered_df[filtered_df["label"] == selected_intent]
      else:
        st.warning("⚠️ 'label' column not found in CSV.")

      if "text" in filtered_df.columns and "record_id" in filtered_df.columns:
        text_to_row = {}
        sentence_options = []
        for _, row in filtered_df.iterrows():
          txt = str(row.get("text", "")).strip()
          rec_id = str(row.get("record_id", "")).strip()
          if txt:
            sentence_options.append(txt)
            text_to_row[txt] = rec_id

        if sentence_options:
          selected_text = st.selectbox("Select a sentence:", sentence_options)

          if selected_text:
            text = selected_text
            rec_id = text_to_row.get(selected_text, "")
            st.caption(
                "<span style='font-size: 0.8em; color: gray;'>Record ID:"
                f" {rec_id}</span>",
                unsafe_allow_html=True,
            )
          else:
            text = ""
        else:
          st.warning("⚠️ No sentences found for the selected filter.")
          text = st.text_area("Enter text in the model language")
      else:
        st.error("❌ 'text' or 'record_id' columns missing from CSV.")
        text = st.text_area("Enter text in the model language")

  else:
    text = st.text_area("Enter text in the model language")

  if st.button("Predict", type="primary"):
    if not text.strip():
      st.info("Enter text first.")
      st.stop()
    try:
      label = pack["model"].predict([text])[0]
      st.subheader(f"The intention of the user is: {label}")
      proba = pack["model"].predict_proba([text])[0]
      max_proba = float(max(proba))
      st.write(f"Model probability (uncalibrated): {max_proba:.1%}")

      st.session_state.history.insert(
          0,
          {
              "timestamp": datetime.now().strftime("%H:%M:%S"),
              "text": text,
              "predicted_intent": label,
              "confidence": max_proba,
          },
      )
    except Exception as e:
      st.error(f"❌ Prediction failed: {e}")

with tab_eval:
  st.header("📊 Model Evaluation Results & Error Analysis")

  st.subheader("Performance Metrics")
  metric_col1, metric_col2 = st.columns(2)
  with metric_col1:
    st.metric("Dev Accuracy", "0.901", "Macro-F1: 0.897")
  with metric_col2:
    st.metric("Test Accuracy", "0.909", "Macro-F1: 0.906")

  st.markdown("---")
  st.subheader("✅ Successful Examples")
  st.markdown("""
1. **`Kesha sa taata?`** (Will it rain today?) — **Gold/Pred:** `weather_query` (High confidence due to weather keyword *kesha*).
2. **`Kesaaja tenakata?`** (What time is it?) — **Gold/Pred:** `datetime_query` (Correctly identified via time marker *saa aja*).
3. **`Inyoyieki saa tomon enkakenya`** (Wake me at 10 AM) — **Gold/Pred:** `alarm_set` (Correctly recognized alarm context).
""")

  st.subheader("❌ Real Failures & Error Analysis")
  st.markdown("""
1. **Input:** *`Tiakaki naduo tokiting' nainyang'uni`* ("tell me the things I'm going to buy")
   - **Gold:** `lists_query` | **Predicted:** `lists_createoradd`
   - **Explanation:** Both list intents share long shopping noun phrases (*ntokitin … nainyangu*). The short verb distinguishing reading versus adding is outweighed by shared character n-grams.
2. **Input:** *`Ntadamuaki nkolati eduo taata`* ("remind me of today's plans")
   - **Gold:** `calendar_query` | **Predicted:** `calendar_set`
   - **Explanation:** *Ntadamuaki* ("remind me") predominantly appears in calendar_set training sentences, causing confusion when used for querying schedules.
""")

with tab_dataset:
  st.header("📋 Dataset Summary & Quality Report")

  st.markdown("""
- **Primary Language:** Maasai (`mas`), mixed Kenyan Maa sections (Kaputiei, Kajiado, Purko, Matapato, Kisongo)
- **Total Records:** 1,024 original human-authored records (Split: 687 train, 172 dev, 165 test)
- **Independent Review:** 1,024 of 1,024 records independently reviewed by reviewer R01.
- **Licence:** CC-BY-4.0 (proposed; release terms pending)
""")

  st.subheader("Intent Distribution Table")
  data_dist = {
      "Intent": [
          "weather_query",
          "datetime_query",
          "alarm_set",
          "calendar_set",
          "calendar_query",
          "lists_createoradd",
          "lists_query",
          "play_music",
          "news_query",
          "qa_definition",
      ],
      "Train": [70, 66, 78, 72, 75, 68, 62, 59, 67, 70],
      "Dev": [18, 17, 20, 16, 18, 16, 17, 16, 17, 17],
      "Test": [19, 16, 18, 15, 16, 16, 18, 15, 16, 16],
      "Total": [107, 99, 116, 103, 109, 100, 97, 90, 100, 103],
  }
  st.table(pd.DataFrame(data_dist))