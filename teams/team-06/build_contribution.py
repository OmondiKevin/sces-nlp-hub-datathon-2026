import pandas as pd, os, sys

SRC = "REVIEW_LOG.csv"
OUT = "data/contribution.csv"

if not os.path.exists(SRC):
    print(f"ERROR: {SRC} not found in this folder. Put your review log here, named REVIEW_LOG.csv")
    sys.exit(1)

df = pd.read_csv(SRC, dtype=str)
print("Columns found in your review log:")
for c in df.columns:
    print("  -", repr(c))

# Rename columns we know for sure
rename = {
    "candidate_id": "record_id",
    "intent_label": "label",
    "Reviewer code": "reviewer_code",
}
# Find the Luganda utterance column no matter its exact header
for c in df.columns:
    if c not in rename and "luganda" in c.lower() and "utterance" in c.lower():
        rename[c] = "text"
df = df.rename(columns=rename)

required = ["record_id", "language", "text", "label", "split", "reviewer_code"]
missing = [c for c in required if c not in df.columns]
if missing:
    print("\nERROR: missing columns after rename:", missing)
    print("Look at the 'Columns found' list above, then tell your doc helper the exact name.")
    sys.exit(1)

df["source_dataset"]        = "team_authored"
df["source_version"]        = "v1"
df["source_record_id"]      = df["record_id"]
df["source_url"]            = "not_applicable"
df["source_method"]         = "original_human"    # change only if Poni says she localised
df["licence_or_permission"] = "documented_contributor_permission"
df["contributor_code"]      = "T06-A"
df["review_status"]         = "independently_reviewed"
df["group_id"]              = df["record_id"]

cols = ["record_id","language","text","label","source_dataset","source_version",
        "source_record_id","source_url","source_method","licence_or_permission",
        "contributor_code","reviewer_code","review_status","group_id","split"]
out = df[cols].copy()

for c in ["text","label","split","language","record_id","reviewer_code"]:
    out[c] = out[c].astype(str).str.strip()

print("\nRow count:", len(out))
print("Split counts:\n", out["split"].value_counts())
print("\nTest counts per label:\n", out[out["split"]=="test"].groupby("label").size())
print("\nDuplicate texts:", int(out["text"].duplicated().sum()))

os.makedirs("data", exist_ok=True)
out.to_csv(OUT, index=False, encoding="utf-8")
print(f"\nWrote {OUT}")