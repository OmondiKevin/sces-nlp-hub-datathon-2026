"""Team 19 final build from the team-reviewed sheet.

  python team19_final.py "<new text for T19-SW-065 or ''>"

Reads data/source/Team19_Kiswahili_250_reviewed.xlsx (Data Entry), fills the provenance fields,
writes data/contribution.csv and data/review_changes.csv, then runs validate -> train -> evaluate.
"""
import sys, subprocess
from pathlib import Path
import openpyxl, pandas as pd
from validate import FIELDS

HERE = Path(__file__).parent
def _pick(*paths):
    return next((Path(p) for p in paths if Path(p).exists()), Path(paths[-1]))
REVIEWED = _pick(r'C:\Users\Harry\Downloads\Team19_Kiswahili_250_MARKED_cleaned.xlsx',
                 HERE / 'data' / 'source' / 'Team19_Kiswahili_250_reviewed.xlsx')
ORIGINAL = _pick(r'C:\Users\Harry\Downloads\Team19_Kiswahili_250_Record_Template (87)-done.xlsx',
                 HERE / 'data' / 'source' / 'Team19_Kiswahili_250_first_draft.xlsx')
LICENCE = 'CC-BY-4.0; Team 19 members consented to NLP Hub Datathon 2026 use'
AUTHOR = 'T19-TEAM'      # written by Harry Sigei (T19-A) and Michael Majau; per-sentence writer not recorded
REVIEWER = 'T19-EN'      # Ezra Ntwiga: independent review of the test split
SELF = 'T19-TEAM'


def sheet(path):
    ws = openpyxl.load_workbook(path)['Data Entry']
    hdr = [c.value for c in ws[1]]
    df = pd.DataFrame([dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True) if r[0]])
    return df.reindex(columns=FIELDS).fillna('').astype(str)


def build(new065):
    df = sheet(REVIEWED)
    df['text'] = df.text.str.replace(r'\s+', ' ', regex=True).str.strip()
    if new065.strip():
        df.loc[df.record_id == 'T19-SW-065', 'text'] = new065.strip()
    df['language'] = 'sw-KE'
    df['source_dataset'] = 'team_authored'
    df['source_method'] = 'original_human'
    df['source_url'] = 'not_applicable'
    df['source_version'] = df.source_version.where(df.source_version != '', 'v1.0')
    df['source_record_id'] = df.record_id
    df['group_id'] = df.record_id
    df['licence_or_permission'] = LICENCE
    df['contributor_code'] = AUTHOR
    test = df.split.eq('test')
    df['reviewer_code'] = SELF
    df.loc[test, 'reviewer_code'] = REVIEWER
    df['review_status'] = 'self_reviewed'
    df.loc[test, 'review_status'] = 'independently_reviewed'
    out = HERE / 'data' / 'contribution.csv'
    df[FIELDS].to_csv(out, index=False, encoding='utf-8')

    # change log: first draft vs reviewed version, with the review reason from the Fix List sheet
    old = sheet(ORIGINAL).set_index('record_id')
    reasons = {}
    try:
        fl = openpyxl.load_workbook(REVIEWED)['Fix List']
        reasons = {r[0]: r[5] for r in fl.iter_rows(min_row=2, values_only=True) if r[0]}
    except KeyError:
        pass
    log = []
    for _, r in df.iterrows():
        o = old.loc[r.record_id] if r.record_id in old.index else None
        ot = '' if o is None else ' '.join(str(o.text).split())
        if o is None or ot != r.text or o.label != r.label:
            action = 'rewritten by team' if ot.casefold() != r.text.casefold() and len(set(ot.split()) & set(r.text.split())) < 2 else 'corrected'
            log.append([r.record_id, r.label, r.split, ot, r.text, action, reasons.get(r.record_id, 'typo / formatting')])
    pd.DataFrame(log, columns=['record_id', 'label', 'split', 'first_draft_text', 'final_text', 'action', 'review_reason']) \
      .to_csv(HERE / 'data' / 'review_changes.csv', index=False, encoding='utf-8')
    print(len(df), 'records ->', out, '|', len(log), 'changed rows logged')


def run(*args):
    print('$ python', ' '.join(args))
    import os
    r = subprocess.run([sys.executable, *args], cwd=HERE, text=True, capture_output=True, encoding='utf-8',
                       env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'})
    print(r.stdout[-3000:], r.stderr[-3000:])
    if r.returncode:
        sys.exit(f'FAILED: {args[0]}')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else '')
    for step in ('validate.py', 'train.py', 'evaluate.py'):
        run(step, '--track', 'intent', '--data', 'data/contribution.csv')
