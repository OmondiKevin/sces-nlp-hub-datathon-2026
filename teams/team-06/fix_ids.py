import pandas as pd

# 1. Read the original log
df = pd.read_csv("REVIEW_LOG.csv", dtype=str)
df['candidate_id'] = df['candidate_id'].astype(str)

# 2. Find duplicates and append _2, _3, etc. to the second/third occurrences
counts = df.groupby('candidate_id').cumcount()
df['candidate_id'] = df['candidate_id'].where(
    counts == 0, 
    df['candidate_id'] + '_' + (counts + 1).astype(str)
)

# 3. Save it back to the original file
df.to_csv("REVIEW_LOG.csv", index=False)
print("Success! All duplicate IDs have been made unique.")