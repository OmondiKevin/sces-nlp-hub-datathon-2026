import pandas as pd
df = pd.read_csv('artifacts/intent/test_predictions.csv')
errors = df[df['label'] != df['predicted']]
print(errors[['record_id', 'text', 'label', 'predicted']].to_string())