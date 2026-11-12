"""Apply a REAL reviewer's verdicts from Review_List.xlsx to data/contribution.csv.
Only rows with a verdict are touched. OK/FIX -> independently_reviewed; DROP -> removed and logged.
Blank verdict -> row unchanged (stays self_reviewed). Usage: python apply_review.py Review_List.xlsx [--code T10-R1]"""
import argparse, csv, re, unicodedata, openpyxl, pandas as pd
def key(s):
    s=unicodedata.normalize('NFD',s or '');s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]','',s.lower())
ap=argparse.ArgumentParser(); ap.add_argument('xlsx'); ap.add_argument('--code',default='T10-R1'); ap.add_argument('--csv',default='data/contribution.csv'); a=ap.parse_args()
df=pd.read_csv(a.csv,dtype=str,keep_default_na=False).set_index('record_id')
log=[];n_ok=n_fix=n_drop=0
for ws in openpyxl.load_workbook(a.xlsx):
    for r in list(ws.iter_rows(min_row=2,values_only=True)):
        rid,_,_,_,verdict,fix=r[:6]; v=(verdict or '').strip().upper()
        if not v or rid not in df.index: continue
        if v=='DROP': log.append((rid,'dropped by reviewer')); df=df.drop(rid); n_drop+=1; continue
        if v=='FIX':
            if not (fix or '').strip(): continue
            if key(fix)==key(df.loc[rid,'text']): n_ok+=1   # only diacritics/spacing differ: treated as OK, original text kept
            else: df.loc[rid,'text']=re.sub(r'\s+',' ',fix).strip(); n_fix+=1
        elif v=='OK': n_ok+=1
        else: continue
        df.loc[rid,['reviewer_code','review_status']]=[a.code,'independently_reviewed']
df.reset_index().to_csv(a.csv,index=False)
if log:
    with open('data/exclusion_log.csv','w',newline='',encoding='utf-8') as f: csv.writer(f).writerows([('record_id','reason')]+log)
print(f'OK {n_ok} | FIX {n_fix} | DROP {n_drop} | independently reviewed now: {(df.review_status=="independently_reviewed").sum()} | rows left: {len(df)}')
