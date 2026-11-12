"""Mobile web interface for the intent track. Serves the REAL trained model (artifacts/intent/model.joblib).
Standard library plus the kit's own dependencies. Run: python mobile_app.py [--host 0.0.0.0] [--port 8501]."""
import argparse, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import joblib, pandas as pd
from core import FRIENDLY, labels

OUT = Path('artifacts/intent')
pack = joblib.load(OUT / 'model.joblib')
model = pack['model']
CLASSES = list(model.classes_)
metrics = json.loads((OUT / 'test_metrics.json').read_text(encoding='utf-8'))
preds = pd.read_csv(OUT / 'test_predictions.csv')

ACTIONS = {  # simulated only; nothing is executed
    'weather_query': 'Would fetch the forecast for the place and day you mentioned.',
    'datetime_query': 'Would read out the current date or time.',
    'alarm_set': 'Would create an alarm at the time you asked for.',
    'calendar_set': 'Would add a new event to your calendar.',
    'calendar_query': 'Would read out your existing calendar events.',
    'lists_createoradd': 'Would create a list or add an item to it.',
    'lists_query': 'Would read out the contents of your list.',
    'play_music': 'Would start playing music.',
    'news_query': 'Would read the latest headlines.',
    'qa_definition': 'Would look up the meaning of the word or concept.'}

# Reading of each real test error, based on the model's strongest n-gram evidence and probabilities.
WHY = {
    'LG-WEA-021': 'Rare words ("okulabula", "ennyandagala") gave little weather evidence. The strongest n-grams were "ag\'" and "ul", which the model links to news. Scores were 0.11 (correct) vs 0.15 (chosen): nearly a coin-flip.',
    'LG-DAT-024': '"Mbuulira" ("tell me") also starts news requests. The model keyed on "buul/lir" and underweighted "essaawa" (time), which is rare in training.',
    'LG-CAL-022_2': 'Both calendar intents share "kalenda". The cue that this is a question about an existing event ("lucyali ku kalenda") is subtle for a character model. It chose calendar_set 0.22 to 0.19.',
    'LG-LIS-023_2': 'The sentence says sugar "has been added" to a list, with a question mark. The gold label lists_query is arguable, so this may be a label-boundary problem and not only a model error. Suggest a second reviewer look at it.',
    'LG-LIS-024_2': '"Laga" ("show") is the only cue for reading a list, and it is rare in training. "olukalala" (list) is shared by both list intents, so the model fell back on add-to-list, 0.21 to 0.17.'}


def classify(text):
    pr = model.predict_proba([text])[0]
    order = sorted(range(len(CLASSES)), key=lambda i: -pr[i])[:3]
    top = [{'label': CLASSES[i], 'name': FRIENDLY[CLASSES[i]], 'p': round(float(pr[i]), 4)} for i in order]
    return {'label': top[0]['label'], 'name': top[0]['name'], 'p': top[0]['p'], 'top': top,
            'action': ACTIONS[top[0]['label']], 'low_confidence': top[0]['p'] < 0.25, 'simulated': True}


def summary():
    rep = metrics['model']['report']
    ok = preds[preds.label == preds.predicted]
    bad = preds[preds.label != preds.predicted]
    return {'n': metrics['test_size'], 'acc': metrics['model']['accuracy'], 'f1': metrics['model']['macro_f1'],
            'base_f1': metrics['majority_baseline']['macro_f1'], 'language': pack['language'],
            'per_label': [{'label': l, 'name': FRIENDLY[l], 'f1': rep[l]['f1-score'], 'n': int(rep[l]['support'])} for l in labels('intent')],
            'correct': [{'text': r.text, 'name': FRIENDLY[r.label]} for r in ok.itertuples()],
            'errors': [{'id': r.record_id, 'text': r.text, 'gold_name': FRIENDLY[r.label], 'pred_name': FRIENDLY[r.predicted],
                        'p': classify(r.text)['p'], 'why': WHY.get(r.record_id, '')} for r in bad.itertuples()]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self._send(200, Path('mobile/index.html').read_bytes(), 'text/html; charset=utf-8')
        elif self.path == '/api/summary':
            self._send(200, json.dumps(summary(), ensure_ascii=False).encode(), 'application/json; charset=utf-8')
        else:
            self._send(404, b'Not found', 'text/plain')

    def do_POST(self):
        if self.path != '/api/predict':
            return self._send(404, b'Not found', 'text/plain')
        try:
            text = json.loads(self.rfile.read(min(int(self.headers.get('Content-Length', 0)), 4096)))['text'].strip()
        except Exception:
            return self._send(400, b'{"error":"bad request"}', 'application/json')
        if not text:
            return self._send(400, b'{"error":"empty"}', 'application/json')
        self._send(200, json.dumps(classify(text[:500]), ensure_ascii=False).encode(), 'application/json; charset=utf-8')

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8501)
    a = ap.parse_args()
    print(f'Serving on http://{a.host}:{a.port} (use --host 0.0.0.0 to open from a phone on the same Wi-Fi)')
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()
