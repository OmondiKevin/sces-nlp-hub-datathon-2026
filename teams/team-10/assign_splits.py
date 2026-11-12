"""Team 10 helper: assign train/dev/test splits for the sentiment track.

Usage:  python assign_splits.py data/contribution.csv           (writes the splits in place)
        python assign_splits.py data/contribution.csv --dry-run (only prints the counts)

Rules it follows (from the datathon handbook / validate.py):
- per label: 60 train, 20 dev, 20 test; any extra rows go to train
- all rows sharing a group_id stay in the same split
- a group may go to test only if EVERY row in it is independently_reviewed
  (reviewer_code differs from contributor_code)
It does not judge language quality. Run validate.py afterwards.
"""
import argparse, random
import pandas as pd

TARGET = {'test': 20, 'dev': 20, 'train': 60}
LABELS = ['positive', 'negative', 'neutral']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--seed', type=int, default=10)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    df = pd.read_csv(a.csv, dtype=str, keep_default_na=False)
    if df.empty:
        raise SystemExit('No rows yet.')
    rnd = random.Random(a.seed)
    df['split'] = ''
    ok_test = (df.review_status == 'independently_reviewed') & (df.reviewer_code != df.contributor_code) & (df.reviewer_code.str.strip() != '')
    for label in LABELS:
        sub = df[df.label == label]
        groups = {g: list(ix) for g, ix in sub.groupby('group_id').groups.items()}
        order = list(groups); rnd.shuffle(order)
        counts = {'test': 0, 'dev': 0}
        for g in order:
            ix = groups[g]
            for split in ('test', 'dev'):
                fits = counts[split] + len(ix) <= TARGET[split]
                eligible = split != 'test' or bool(ok_test[ix].all())
                if fits and eligible:
                    df.loc[ix, 'split'] = split; counts[split] += len(ix); break
            else:
                df.loc[ix, 'split'] = 'train'
    summary = df.groupby(['label', 'split']).size().unstack(fill_value=0).reindex(columns=['train', 'dev', 'test'], fill_value=0)
    print(summary)
    short = [(l, s) for l in LABELS for s in TARGET if (l in summary.index and summary.loc[l, s] < TARGET[s]) or l not in summary.index]
    if short:
        print('\nBelow the minimum for:', ', '.join(f'{l}/{s}' for l, s in short),
              '\n(write or review more sentences; test needs independently reviewed rows)')
    if not a.dry_run:
        df.to_csv(a.csv, index=False)
        print('\nSplits written to', a.csv)

if __name__ == '__main__':
    main()
