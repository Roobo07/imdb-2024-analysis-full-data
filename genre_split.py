import pandas as pd
import os

INPUT_FILE = "data/processed/imdb_2024_cleaned.csv"
OUTPUT_DIR = "data/raw"

def split_by_genre():
    # Load cleaned data
    df = pd.read_csv(INPUT_FILE)

    print("Total movies:", len(df))

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Split multi-genre rows into multiple rows
    df["genre"] = df["genre"].str.split(",")

    df = df.explode("genre")
    df["genre"] = df["genre"].str.strip().str.lower()

    # Create one CSV per genre
    for genre_name, genre_df in df.groupby("genre"):
        file_path = os.path.join(OUTPUT_DIR, f"{genre_name}.csv")
        genre_df.to_csv(file_path, index=False)
        print(f"✅ Saved {genre_name}.csv → {len(genre_df)} movies")

    print("🎉 Genre split completed!")


if __name__ == "__main__":
    split_by_genre()
