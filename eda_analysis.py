import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
DATA_FILE = "data/processed/imdb_2024_cleaned.csv"
OUTPUT_DIR = "eda_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)

top_movies = (
    df[df["votes"] > 10000]
    .sort_values(by="rating", ascending=False)
    .head(10)
)

plt.figure()
plt.barh(top_movies["movie_name"], top_movies["rating"])
plt.xlabel("Rating")
plt.title("Top 10 Movies by Rating (Votes > 10k)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_10_movies.png")
plt.close()
genre_df = df.copy()
genre_df["genre"] = genre_df["genre"].str.split(",")
genre_df = genre_df.explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()

genre_counts = genre_df["genre"].value_counts().head(10)

plt.figure()
genre_counts.plot(kind="bar")
plt.ylabel("Number of Movies")
plt.title("Top 10 Genres by Movie Count")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/genre_distribution.png")
plt.close()

duration_genre = (
    genre_df.groupby("genre")["duration_minutes"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
duration_genre.plot(kind="barh")
plt.xlabel("Average Duration (minutes)")
plt.title("Average Movie Duration by Genre")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/avg_duration_by_genre.png")
plt.close()

plt.figure()
plt.hist(df["rating"].dropna(), bins=20)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.title("Rating Distribution (IMDb 2024)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/rating_distribution.png")
plt.close()

plt.figure()
plt.hist(df["votes"].dropna(), bins=30)
plt.xlabel("Votes")
plt.ylabel("Count")
plt.title("Voting Distribution")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/voting_distribution.png")
plt.close()

plt.figure()
plt.scatter(df["votes"], df["rating"])
plt.xlabel("Votes")
plt.ylabel("Rating")
plt.title("Rating vs Voting Count")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/rating_vs_votes.png")
plt.close()

print("✅ EDA charts saved in eda_outputs folder")
