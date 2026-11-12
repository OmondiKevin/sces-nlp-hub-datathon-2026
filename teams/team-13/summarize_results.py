"""Derive tables/errors from actual frozen test predictions; never invent explanations."""
import json
from pathlib import Path
import joblib,pandas as pd
from core import fingerprint

if __name__=='__main__':
    out=Path('artifacts/intent')
    pack=joblib.load(out/'model.joblib')
    if pack['practice'] or pack['language']!='ki':raise SystemExit('Refusing to present a practice/non-Kikuyu model as Team 13 results.')
    df=pd.read_csv('data/contribution.csv',dtype=str,keep_default_na=False)
    if fingerprint(df)!=pack['data_sha256']:raise SystemExit('Dataset changed since training.')
    metrics=json.loads((out/'test_metrics.json').read_text(encoding='utf-8'))
    if metrics['practice']:raise SystemExit('Practice metrics cannot be Kikuyu results.')
    score=metrics['model']
    pd.DataFrame(score['confusion_matrix'],index=score['label_order'],columns=score['label_order']).to_csv(out/'confusion_matrix.csv')
    preds=pd.read_csv(out/'test_predictions.csv',keep_default_na=False)
    errors=preds[preds.label!=preds.predicted]
    errors.head(5).assign(human_error_analysis='PENDING human inspection').to_csv(out/'errors_for_review.csv',index=False)
    text=f"# Actual Kikuyu test results\n\nTest size: {metrics['test_size']}. Accuracy: {score['accuracy']:.4f}. Macro-F1: {score['macro_f1']:.4f}.\n\nMajority accuracy: {metrics['majority_baseline']['accuracy']:.4f}; macro-F1: {metrics['majority_baseline']['macro_f1']:.4f}.\n\nObserved mistakes: {len(errors)}. Up to five are saved in errors_for_review.csv for human explanation. No causes are inferred automatically.\n\nDataset fingerprint: {pack['data_sha256']}. Model probabilities are uncalibrated. Do not tune against these test results.\n"
    (out/'RESULTS.md').write_text(text,encoding='utf-8');print(text)
