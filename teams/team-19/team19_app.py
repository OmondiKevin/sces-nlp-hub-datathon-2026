"""Team 19 · Kiswahili intent demo (adapted from the starter-kit app.py).

Run:  python -m streamlit run team19_app.py
Shows real predictions from artifacts/intent/model.joblib, the frozen test results,
actual failure cases and the dataset. No real action (alarm, calendar, music...) is executed.

Design concept: "a living phrasebook". Each request is read like a dictionary entry:
the sentence is the headword, the intent is its definition, and the model's full
probability ledger is printed beneath it, so uncertainty is part of the reading.
"""
import html
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from core import FRIENDLY, INTENTS, fingerprint

ROOT = Path(__file__).parent
ART = ROOT / 'artifacts' / 'intent'
DATA = ROOT / 'data' / 'contribution.csv'
CHANGES = ROOT / 'data' / 'review_changes.csv'

SW = {  # Kiswahili name, simulated assistant reply (no real action is taken)
    'weather_query': ('Hali ya hewa', 'Ningekuonyesha utabiri wa hali ya hewa.'),
    'datetime_query': ('Tarehe au saa', 'Ningekuambia tarehe au saa uliyouliza.'),
    'alarm_set': ('Weka kengele', 'Ningekuwekea kengele.'),
    'calendar_set': ('Ongeza kwenye kalenda', 'Ningeongeza tukio hili kwenye kalenda yako.'),
    'calendar_query': ('Angalia kalenda', 'Ningesoma matukio yaliyo kwenye kalenda yako.'),
    'lists_createoradd': ('Ongeza kwenye orodha', 'Ningeongeza kipengee hiki kwenye orodha yako.'),
    'lists_query': ('Soma orodha', 'Ningekusomea orodha yako.'),
    'play_music': ('Cheza muziki', 'Ningekuchezea muziki huo.'),
    'news_query': ('Habari', 'Ningekuletea habari za hivi punde.'),
    'qa_definition': ('Maana ya neno', 'Ningekueleza maana ya neno hilo.'),
}
NUM = {l: f'{i + 1:02d}' for i, l in enumerate(INTENTS)}  # index numbers instead of icons
EXAMPLES = ['Niamshe saa kumi na mbili', 'Weka wimbo wa Sauti Sol', 'Ongeza maziwa kwenye orodha ya sokoni',
            'Habari za Gor Mahia leo?', 'Maana ya neno upendo ni nini?', 'Nina meeting gani kesho?']
e = html.escape

st.set_page_config(page_title='Msaidizi · Team 19', layout='wide')
st.markdown("""
<style>
:root { color-scheme:dark; }
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root {
  --paper:#121110; --surface:#1b1a18; --ink:#ece8df; --ink-2:#a39d90; --hair:#2e2b27; --hair-2:#4a453d;
  --accent:#ef6a52; --accent-soft:#3a1c17; --ok:#7fb38a;
  --serif:'Fraunces', Georgia, serif; --sans:'IBM Plex Sans', system-ui, sans-serif; --mono:'IBM Plex Mono', ui-monospace, monospace;
  --ease:cubic-bezier(0.16, 1, 0.3, 1); --dur:280ms;
}
html, body, .stApp, .stMarkdown, button, input, textarea, select, label, p, li { font-family:var(--sans) !important; }
.stApp { background:var(--paper); color:var(--ink); }
.block-container { padding-top:2.2rem; max-width:1120px; }
code { font-family:var(--mono) !important; background:transparent !important; color:var(--ink-2) !important; font-size:.82em; }
h1, h2, h3 { font-family:var(--serif) !important; font-weight:600; color:var(--ink); letter-spacing:-.015em; }

/* Masthead */
.mast { display:grid; grid-template-columns:1fr auto; align-items:end; gap:1rem;
        border-bottom:1px solid var(--ink); padding-bottom:1rem; margin-bottom:.4rem; }
.mast h1 { font-size:clamp(2.4rem, 5vw, 3.6rem); line-height:1; margin:0; font-weight:400; }
.mast h1 em { font-style:italic; color:var(--accent); }
.mast .dek { color:var(--ink-2); margin:.6rem 0 0; max-width:46ch; font-size:1rem; }
.meta { font-family:var(--mono); font-size:.74rem; color:var(--ink-2); text-align:right; line-height:1.7;
        text-transform:uppercase; letter-spacing:.06em; }
.meta b { color:var(--ink); font-weight:500; }

/* Tabs as a running header */
.stTabs [data-baseweb="tab-list"] { gap:1.6rem; border-bottom:1px solid var(--hair); }
.stTabs [data-baseweb="tab"] { padding:.7rem 0; font-family:var(--mono) !important; font-size:.78rem;
        text-transform:uppercase; letter-spacing:.08em; color:var(--ink-2); }
.stTabs [aria-selected="true"] { color:var(--ink); }
.stTabs [data-baseweb="tab-highlight"] { background:var(--accent); height:2px; }

/* Controls */
.label { font-family:var(--mono); font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--ink-2); margin:1.4rem 0 .5rem; }
.stButton > button { border-radius:0; border:1px solid var(--hair-2); background:var(--surface); color:var(--ink);
        font-weight:400; text-align:left; justify-content:flex-start; min-height:2.8rem;
        transition:border-color var(--dur) var(--ease), background var(--dur) var(--ease); }
.stButton > button:hover { border-color:var(--ink); background:var(--hair); color:var(--ink); }
.stButton > button:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
.stTextInput input { border-radius:0; background:var(--surface); font-family:var(--serif) !important;
        font-size:1.35rem; padding:.9rem 1rem; color:var(--ink); }
.stTextInput label p { font-family:var(--mono) !important; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--ink-2); }

/* Entry (the signature) */
.entry { border-top:1px solid var(--ink); margin-top:1.6rem; padding-top:1.4rem; animation:rise var(--dur) var(--ease) both; }
.head { font-family:var(--serif); font-size:clamp(1.6rem, 3.4vw, 2.3rem); line-height:1.15; margin:0 0 .35rem; }
.pos { font-family:var(--mono); font-size:.78rem; color:var(--ink-2); letter-spacing:.04em; }
.pos .n { color:var(--accent); }
.def { font-size:1.05rem; margin:1rem 0 .2rem; }
.def b { font-family:var(--serif); font-size:1.5rem; font-weight:600; }
.reply { border-left:2px solid var(--hair-2); padding:.2rem 0 .2rem 1rem; margin-top:1rem; color:var(--ink-2); font-style:italic; }
.reply span { display:block; font-style:normal; font-family:var(--mono); font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.2rem; }
.note { margin-top:1rem; padding:.7rem .9rem; background:var(--accent-soft); color:#f4b9ad; font-size:.9rem; }
.ledger { width:100%; border-collapse:collapse; font-size:.9rem; }
.ledger td { padding:.42rem 0; border-bottom:1px solid var(--hair); vertical-align:middle; }
.ledger .n { font-family:var(--mono); font-size:.72rem; color:var(--ink-2); width:2.2rem; }
.ledger .p { font-family:var(--mono); font-size:.8rem; text-align:right; width:3.4rem; font-variant-numeric:tabular-nums; }
.ledger .bar { width:38%; padding-left:1rem; }
.ledger .bar i { display:block; height:3px; background:var(--hair-2); transform-origin:left; animation:grow 600ms var(--ease) both; }
.ledger tr.win td { color:var(--ink); font-weight:600; }
.ledger tr.win .bar i { background:var(--accent); height:5px; }
.ledger tr:not(.win) td { color:var(--ink-2); }

/* Figures */
.fig { display:grid; grid-template-columns:repeat(4, 1fr); border-top:1px solid var(--ink); border-bottom:1px solid var(--hair); margin:1.4rem 0; }
.fig div { padding:1rem 1rem 1.1rem 0; }
.fig div + div { border-left:1px solid var(--hair); padding-left:1rem; }
.fig .v { font-family:var(--serif); font-size:2.4rem; line-height:1; font-variant-numeric:tabular-nums; }
.fig .v.acc { color:var(--accent); }
.fig .k { font-family:var(--mono); font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; color:var(--ink-2); margin-top:.5rem; }
.caption { color:var(--ink-2); font-size:.86rem; max-width:70ch; }
.err { border-bottom:1px solid var(--hair); padding:.9rem 0; display:grid; grid-template-columns:1fr auto; gap:1rem; }
.err .s { font-family:var(--serif); font-size:1.15rem; }
.err .w { font-family:var(--mono); font-size:.76rem; text-align:right; color:var(--ink-2); white-space:nowrap; }
.err .w s { color:var(--ink-2); } .err .w b { color:var(--accent); font-weight:500; }
.prose { max-width:64ch; font-size:1rem; line-height:1.65; }
.prose h3 { font-size:1.35rem; margin-top:1.6rem; }
[data-testid="stDataFrame"] { border:1px solid var(--hair); }

@keyframes rise { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }
@keyframes grow { from { transform:scaleX(0); } to { transform:scaleX(1); } }
@media (prefers-reduced-motion: reduce) { .entry, .ledger .bar i { animation:none; } }
@media (max-width: 720px) { .mast { grid-template-columns:1fr; } .meta { text-align:left; } .fig { grid-template-columns:1fr 1fr; }
  .fig div:nth-child(3) { border-left:0; padding-left:0; } }
</style>""", unsafe_allow_html=True)


@st.cache_resource
def load_pack():
    return joblib.load(ART / 'model.joblib')  # our own trained file; never load untrusted joblib


@st.cache_data
def load_data():
    df = pd.read_csv(DATA, dtype=str).fillna('')
    ch = pd.read_csv(CHANGES, dtype=str).fillna('') if CHANGES.exists() else pd.DataFrame()
    test = json.loads((ART / 'test_metrics.json').read_text(encoding='utf-8'))
    preds = pd.read_csv(ART / 'test_predictions.csv', dtype=str).fillna('')
    return df, ch, test, preds


if not (ART / 'model.joblib').exists():
    st.error('No trained model found. Run: python train.py --track intent --data data/contribution.csv'); st.stop()
pack = load_pack(); df, changes, test, preds = load_data()
model = pack['model']; m = test['model']; base = test['majority_baseline']
data_ok = pack['data_sha256'] == fingerprint(pd.read_csv(DATA))

st.markdown(f"""<header class="mast"><div>
<h1>Msaidizi <em>wa</em> Kiswahili</h1>
<p class="dek">What is a Kenyan Kiswahili speaker asking their phone to do? A small, honest model trained on
{len(df)} sentences we wrote ourselves.</p></div>
<div class="meta">Team 19 · Track A<br>Intent · sw-KE<br>Test macro-F1 <b>{m['macro_f1']:.3f}</b></div></header>""",
            unsafe_allow_html=True)
if pack.get('practice'):
    st.warning('Practice-mode model loaded. Scores do not reflect real-world quality.')
if not data_ok:
    st.warning('data/contribution.csv changed after training. Retrain before trusting these results.')

t1, t2, t3, t4 = st.tabs(['Jaribu · Try it', 'Results', 'Dataset', 'About'])

# ---------------- Try it ----------------
with t1:
    if 'q' not in st.session_state:
        st.session_state.q = ''
    st.markdown('<div class="label">Try a sentence</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, ex in enumerate(EXAMPLES):
        if cols[i % 3].button(ex, width='stretch', key=f'ex{i}'):
            st.session_state.q = ex
    text = st.text_input('Or write your own request in Kiswahili', key='q',
                         placeholder='Kesho kutanyesha Nairobi?')
    if not text.strip():
        st.markdown('<p class="caption">Choose an example or type a request. The model reads it and returns one of '
                    'ten intents, along with how strongly it leans toward each.</p>', unsafe_allow_html=True)
    else:
        proba = model.predict_proba([text])[0]
        ranked = sorted(zip(model.classes_, proba), key=lambda x: -x[1])
        lab, p = ranked[0]
        rows = ''.join(
            f"<tr class='{'win' if j == 0 else ''}'><td class='n'>{NUM[l]}</td><td>{SW[l][0]} "
            f"<code>{l}</code></td><td class='bar'><i style='width:{pr * 100:.1f}%'></i></td>"
            f"<td class='p'>{pr:.0%}</td></tr>" for j, (l, pr) in enumerate(ranked))
        unsure = ('<div class="note">The model is unsure. This request may be ambiguous or outside the ten intents. '
                  'It always chooses one of them, even for unrelated input.</div>') if p < 0.30 else ''
        left, right = st.columns([1, 1.05], gap='large')
        with left:
            st.markdown(f"""<article class="entry" aria-live="polite">
<p class="head">“{e(text.strip())}”</p>
<div class="pos"><span class="n">{NUM[lab]}</span> · {lab} · probability {p:.0%} (uncalibrated)</div>
<p class="def"><b>{SW[lab][0]}</b><br>{FRIENDLY[lab]}</p>
<div class="reply"><span>Simulated reply</span>{SW[lab][1]}</div>{unsure}</article>""", unsafe_allow_html=True)
        with right:
            st.markdown(f'<div class="entry"><div class="label" style="margin-top:0">All ten intents, ranked</div>'
                        f'<table class="ledger">{rows}</table></div>', unsafe_allow_html=True)
        st.markdown('<p class="caption" style="margin-top:1.2rem">Simulated route only. No alarm, calendar, music, '
                    'weather or other action is executed.</p>', unsafe_allow_html=True)

# ---------------- Results ----------------
with t2:
    st.markdown(f"""<div class="fig">
<div><div class="v acc">{m['accuracy']:.0%}</div><div class="k">Test accuracy</div></div>
<div><div class="v">{m['macro_f1']:.3f}</div><div class="k">Test macro-F1</div></div>
<div><div class="v">{base['macro_f1']:.3f}</div><div class="k">Majority baseline F1</div></div>
<div><div class="v">{test.get('test_size', len(preds))}</div><div class="k">Held-out sentences</div></div></div>
<p class="caption">Frozen test split, five sentences per intent, evaluated once after all choices were fixed on the
development split. Model: character 2–5-gram TF-IDF with logistic regression, the starter-kit baseline.</p>""",
                unsafe_allow_html=True)
    a, b = st.columns([1.1, 1], gap='large')
    with a:
        st.markdown('<div class="label">F1 by intent</div>', unsafe_allow_html=True)
        f1 = pd.DataFrame({'intent': [f"{NUM[l]} {l}" for l in INTENTS],
                           'F1': [m['report'][l]['f1-score'] for l in INTENTS]}).set_index('intent')
        st.bar_chart(f1, horizontal=True, color='#ece8df', height=360)
    with b:
        st.markdown('<div class="label">Confusion matrix · rows true, columns predicted</div>', unsafe_allow_html=True)
        cm = pd.crosstab(preds['label'], preds['predicted']).reindex(index=INTENTS, columns=INTENTS, fill_value=0)
        cm.index = [f"{NUM[l]} {l}" for l in cm.index]; cm.columns = [NUM[l] for l in cm.columns]
        st.dataframe(cm, width='stretch', height=390)
    err = preds[preds.label != preds.predicted]
    st.markdown(f'<div class="label">Every test mistake ({len(err)})</div>' + ''.join(
        f"<div class='err'><div class='s'>“{e(r.text)}”</div><div class='w'>true <s>{r.label}</s><br>"
        f"model <b>{r.predicted}</b></div></div>" for r in err.itertuples()), unsafe_allow_html=True)
    st.markdown("""<div class="prose"><h3>Why it fails where it does</h3><ul>
<li><b>Lists</b> are the weakest. Adding to a list and asking about one both use <i>orodha</i>, and character
n-grams barely notice the verb that separates them.</li>
<li>A time phrase such as <i>saa mbili asubuhi</i> pulls calendar requests towards <b>alarm</b>.</li>
<li>Unseen technical words such as <i>biometriki</i> give the model nothing to go on.</li></ul></div>""",
                unsafe_allow_html=True)

# ---------------- Dataset ----------------
with t3:
    st.markdown(f"""<div class="fig">
<div><div class="v">{len(df)}</div><div class="k">Sentences</div></div>
<div><div class="v">{df.label.nunique()}</div><div class="k">Intents</div></div>
<div><div class="v">15·5·5</div><div class="k">Train · dev · test per intent</div></div>
<div><div class="v acc">{len(changes) if len(changes) else '–'}</div><div class="k">Rows corrected in review</div></div></div>""",
                unsafe_allow_html=True)
    a, b = st.columns([1, 1.2], gap='large')
    with a:
        st.markdown(f"""<div class="prose"><h3>Provenance</h3><ul>
<li>Written by Harry Sigei and Michael Majau (<code>team_authored</code>, <code>original_human</code>).</li>
<li>Licence: {e(df.licence_or_permission.iloc[0])}.</li>
<li>All 50 test sentences were independently reviewed by Ezra Ntwiga (<code>T19-EN</code>), who wrote none of them.</li>
<li>Every change from the first draft is logged, with a reason, in <code>data/review_changes.csv</code>.</li></ul></div>""",
                    unsafe_allow_html=True)
    with b:
        pick = st.selectbox('Read the sentences for an intent', INTENTS,
                            format_func=lambda l: f"{NUM[l]}  {SW[l][0]} ({l})")
        st.dataframe(df[df.label == pick][['record_id', 'text', 'split', 'review_status']],
                     hide_index=True, width='stretch', height=330)

# ---------------- About ----------------
with t4:
    st.markdown(f"""<div class="prose">
<h3>Team 19</h3>
<p>Harry Sigei (data lead, writing, training, demo), Michael Majau (writing and rewriting), and Ezra Ntwiga
(independent test reviewer).</p>
<h3>Why we built it</h3>
<p>Phone assistants often misunderstand everyday Kenyan Kiswahili. We wrote 250 requests ourselves, 25 for each of ten
intents split 15/5/5, and trained a transparent baseline so the results can be checked and reproduced.</p>
<h3>Limitations</h3><ul>
<li>Small data: 25 sentences per intent from two writers, so probabilities are low and uncalibrated.</li>
<li>The rewritten sentences are more formal than everyday Sheng or code-switched speech.</li>
<li>The model always picks one of the ten intents. It cannot say it does not know.</li>
<li>This is a demonstration: no real alarm, calendar, list, music or news action is executed.</li></ul>
<h3>AI use</h3>
<p>AI tools helped with code, documentation, interface styling and spotting problems in the data. Every dataset
sentence was written and rewritten by team members. See <code>docs/CONTRIBUTIONS.md</code>.</p>
<p class="caption">Data fingerprint (sha256) {pack['data_sha256'][:16]}… · trained on
{len(df[df.split == 'train'])} sentences</p></div>""", unsafe_allow_html=True)
