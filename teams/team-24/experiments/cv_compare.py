# Post-hoc model-comparison experiment. Uses ONLY train+dev rows (5-fold x3 repeated CV). Test rows are never loaded.
import json,itertools,numpy as np,pandas as pd,warnings
warnings.filterwarnings('ignore')
from sklearn.pipeline import make_pipeline,make_union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold,cross_val_score
K=''  # run from the starter-kit folder: python experiments/cv_compare.py
df=pd.read_csv(K+'data/contribution.csv',dtype=str,keep_default_na=False)
df=df[df.split.isin(['train','dev'])]   # test rows are never used in selection
print('rows used:',len(df),df.split.value_counts().to_dict())
X,y=df.text,df.label
def feats(kind):
    ch=lambda:TfidfVectorizer(analyzer='char',ngram_range=(2,5))
    wd=lambda:TfidfVectorizer(analyzer='word',ngram_range=(1,2),token_pattern=r"(?u)\b\w+\b")
    return {'char':ch(),'word':wd(),'char+word':make_union(ch(),wd())}[kind]
cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=3,random_state=42)
res=[]
for kind,C,cw in itertools.product(['char','word','char+word'],[1,10],[None,'balanced']):
    m=make_pipeline(feats(kind),LogisticRegression(C=C,class_weight=cw,max_iter=2000,random_state=42))
    s=cross_val_score(m,X,y,cv=cv,scoring='f1_macro')
    res.append(dict(features=kind,C=C,class_weight=cw,mean=float(s.mean()),sd=float(s.std()),scores=s.tolist()))
base=[r for r in res if r['features']=='char' and r['C']==1 and r['class_weight'] is None][0]
print(f"\nBASELINE (kit settings: char 2-5, C=1, no weights): CV macro-F1 {base['mean']:.3f} +/- {base['sd']:.3f}\n")
for r in sorted(res,key=lambda r:-r['mean']):
    d=np.array(r['scores'])-np.array(base['scores'])
    print(f"{r['features']:10s} C={r['C']:<3d} cw={str(r['class_weight']):9s} {r['mean']:.3f} +/- {r['sd']:.3f}  vs baseline {d.mean():+.3f} (folds better {int((d>0).sum())}/{len(d)})")
json.dump(res,open('experiments/cv_results.json','w'))
