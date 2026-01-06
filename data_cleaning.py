import pandas as pd
import os

RAW_PATH = "data/raw/imdb_2024_raw.csv"
PROCESSED_PATH = "data/processed/imdb_2024_cleaned.csv"

def clean_imdb_data():
    # Load raw data
    df = pd.read_csv(RAW_PATH)

    print("Initial shape:", df.shape)

    # Replace '\N' with NaN
    df.replace("\\N", pd.NA, inplace=True)

    # Convert rating to float
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # Convert votes to integer
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce")

    # Convert duration to integer
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")

    # Drop rows without rating
    df = df.dropna(subset=["rating"])

    # Strip whitespace
    df["movie_name"] = df["movie_name"].str.strip()
    df["genre"] = df["genre"].str.strip()

    print("After cleaning:", df.shape)

    # Ensure processed folder exists
    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned data
    df.to_csv(PROCESSED_PATH, index=False)
    print("✅ Cleaned data saved to:", PROCESSED_PATH)


if __name__ == "__main__":
    clean_imdb_data()
