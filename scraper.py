import pandas as pd
import os

# -----------------------------
# SAFE ABSOLUTE PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")

print("Using data directory:", DATA_RAW)

BASICS_FILE = os.path.join(DATA_RAW, "title.basics.tsv.gz")
RATINGS_FILE = os.path.join(DATA_RAW, "title.ratings.tsv.gz")
OUTPUT_FILE = os.path.join(DATA_RAW, "imdb_2024_raw.csv")

# -----------------------------
# VERIFY FILES EXIST
# -----------------------------
if not os.path.exists(BASICS_FILE):
    raise FileNotFoundError(f"Missing file: {BASICS_FILE}")

if not os.path.exists(RATINGS_FILE):
    raise FileNotFoundError(f"Missing file: {RATINGS_FILE}")

# -----------------------------
# LOAD DATA
# -----------------------------
basics = pd.read_csv(
    BASICS_FILE,
    sep="\t",
    low_memory=False
)

ratings = pd.read_csv(
    RATINGS_FILE,
    sep="\t"
)

# -----------------------------
# FILTER 2024 MOVIES
# -----------------------------
movies_2024 = basics[
    (basics["titleType"] == "movie") &
    (basics["startYear"] == "2024")
]

# -----------------------------
# MERGE RATINGS
# -----------------------------
movies_2024 = movies_2024.merge(
    ratings,
    on="tconst",
    how="left"
)

# -----------------------------
# SELECT & RENAME COLUMNS
# -----------------------------
final_df = movies_2024[[
    "primaryTitle",
    "genres",
    "averageRating",
    "numVotes",
    "runtimeMinutes"
]].rename(columns={
    "primaryTitle": "movie_name",
    "genres": "genre",
    "averageRating": "rating",
    "numVotes": "votes",
    "runtimeMinutes": "duration_minutes"
})

# -----------------------------
# SAVE OUTPUT
# -----------------------------
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ 2024 IMDb movies saved: {len(final_df)}")
print("📄 File created:", OUTPUT_FILE)
