"""Sheet -> contribution.csv for Kiswahili Track C (semantic).
Usage: python make_contribution.py kiswahili_trackC_fixed_items.xlsx contribution.csv
Needs only openpyxl. Offsets are computed here from the text (never typed by hand)."""
import csv, json, random, re, sys, collections, warnings
import openpyxl
warnings.filterwarnings('ignore')

# ---- edit these to match the kit / your team (validate.py is the judge) ----
SOURCE_DATASET   = 'strathmore_team_original'
SOURCE_VERSION   = '1.0'
SOURCE_URL       = 'not_applicable'
METHOD_HUMAN     = 'original_human'   # kit allows: original_human, human_localised, newly_annotated, corrected_with_evidence
METHOD_AI        = 'original_human'
LICENCE          = 'CC0'            # CONFIRM the team agrees to this
REVIEWER_CODE    = 'R1'             # set to the independent reviewer's code; only valid once they have really checked the row
UNREVIEWED_CODE  = 'pending'        # placeholder so required fields are not empty
REVIEW_STATUS    = 'pending'        # kit example uses 'independently_reviewed'
SEED             = 2026
QUOTA            = {'train': 15, 'dev': 5, 'test': 5}   # per intent
VALID = {'location', 'date', 'time', 'item', 'term'}
# -----------------------------------------------------------------------------

src, out = sys.argv[1], sys.argv[2]
ws = openpyxl.load_workbook(src)['Rows']
rows = []
H = {re.sub(r'[^a-z]', '', str(c.value).lower()): c.column for c in ws[1] if c.value}
col = lambda *names: next(H[n] for n in names if n in H)
cT, cI, cS = col('text'), col('intent'), col('slots')
cW, cA = col('writerid'), col('aideclared')
cG = H.get('groupid')
for r in range(2, ws.max_row + 1):
    t, i, s = ws.cell(r, cT).value, ws.cell(r, cI).value, ws.cell(r, cS).value
    w, ai = ws.cell(r, cW).value, ws.cell(r, cA).value
    g = ws.cell(r, cG).value if cG else None
    if not (t and i):
        continue
    spans = []
    for part in (s or '').split(';'):
        part = part.strip()
        if not part:
            continue
        v, ty = part.rsplit('=', 1)
        assert ty in VALID, (r, part)
        ms = list(re.finditer(r'(?<!\w)' + re.escape(v) + r'(?!\w)', t))
        assert len(ms) == 1, f'row {r}: span {v!r} found {len(ms)} times in text'
        m = ms[0]; assert t[m.start():m.end()] == v
        spans.append({'type': ty, 'value': v, 'start': m.start(), 'end': m.end()})
    spans.sort(key=lambda d: d['start'])
    for a, b in zip(spans, spans[1:]):
        assert a['end'] <= b['start'], f'row {r}: overlapping spans'
    rows.append(dict(row=r, text=t, intent=i, spans=spans, writer=w or '', group=g or f'g{r:03d}', ai=(ai == 'yes')))

# groups must not straddle intents
gi = collections.defaultdict(set)
for x in rows: gi[x['group']].add(x['intent'])
assert all(len(v) == 1 for v in gi.values()), [g for g, v in gi.items() if len(v) > 1]

# value frequency across the whole sheet (type, value)
freq = collections.Counter((s['type'], s['value']) for x in rows for s in x['spans'])
def uniq_score(grp):  # how many slot values appear nowhere else
    return sum(1 for x in grp for s in x['spans'] if freq[(s['type'], s['value'])] == 1)

TARGET_CHALLENGE = 20   # test rows allowed to carry a slot value never seen in train
def build(seed):
    rng = random.Random(seed); split = {}
    for intent in sorted({x['intent'] for x in rows}):
        groups = collections.defaultdict(list)
        for x in rows:
            if x['intent'] == intent: groups[x['group']].append(x)
        G = list(groups.values()); rng.shuffle(G)
        # test = human-written only; ~2 high-novelty groups + the rest low-novelty (values that recur elsewhere)
        human = [g for g in G if not any(x['ai'] for x in g)]
        human.sort(key=lambda g: uniq_score(g))
        hi = human[::-1][:rng.randint(1, 3)]
        lo = [g for g in human if g not in hi]; lo = lo[:max(8, len(lo)//2)]; rng.shuffle(lo)
        order = hi + lo + [g for g in G if g not in hi and g not in lo]
        need = dict(QUOTA); take = {'test': [], 'dev': [], 'train': []}; left = list(order)
        for name in ('test', 'dev', 'train'):
            for g in list(left):
                if need[name] >= len(g):
                    take[name].append(g); need[name] -= len(g); left.remove(g)
                if need[name] == 0: break
            if name == 'test': rng.shuffle(left)
        if need != {'train': 0, 'dev': 0, 'test': 0} or left: return None
        for name, gs in take.items():
            for g in gs:
                for x in g: split[x['row']] = name
    return split
def challenge(split):
    tv = {(s['type'], s['value']) for x in rows if split[x['row']] == 'train' for s in x['spans']}
    return sum(1 for x in rows if split[x['row']] == 'test' and any((s['type'], s['value']) not in tv for s in x['spans']))
best = None
for seed in range(SEED, SEED + 400):
    sp = build(seed)
    if sp is None: continue
    t_ai = sum(1 for x in rows if x['ai'] and sp[x['row']] == 'test')
    sc = (t_ai, abs(challenge(sp) - TARGET_CHALLENGE))
    if best is None or sc < best[0]: best = (sc, seed, sp)
split = best[2]; print('seed used:', best[1])

with open(out, 'w', newline='', encoding='utf-8') as f:
    wr = csv.writer(f)
    wr.writerow('record_id,language,text,label,source_dataset,source_version,source_record_id,source_url,source_method,licence_or_permission,contributor_code,reviewer_code,review_status,group_id,split,slots_json'.split(','))
    for n, x in enumerate(rows, 1):
        wr.writerow([f'sw-{n:03d}', 'sw', x['text'], x['intent'], SOURCE_DATASET, SOURCE_VERSION, f"row{x['row']}",
                     SOURCE_URL, METHOD_AI if x['ai'] else METHOD_HUMAN, LICENCE, x['writer'],
                     REVIEWER_CODE if (split[x['row']] == 'test' and REVIEW_STATUS == 'independently_reviewed') else UNREVIEWED_CODE, REVIEW_STATUS, x['group'],
                     split[x['row']], json.dumps(x['spans'], ensure_ascii=False)])

# ---- report ----
by = collections.defaultdict(list)
for x in rows: by[split[x['row']]].append(x)
print({k: len(v) for k, v in by.items()})
trainvals = {(s['type'], s['value']) for x in by['train'] for s in x['spans']}
t = by['test']
print('test rows with slots:', sum(1 for x in t if x['spans']), 'empty:', sum(1 for x in t if not x['spans']))
print('test AI-rephrased rows:', sum(x['ai'] for x in t))
ch = [x for x in t if any((s['type'], s['value']) not in trainvals for s in x['spans'])]
print('test rows with >=1 unseen slot value (challenge subset):', len(ch))
print('test per intent:', dict(collections.Counter(x['intent'] for x in t)))
print('slot rows total:', sum(1 for x in rows if x['spans']))
