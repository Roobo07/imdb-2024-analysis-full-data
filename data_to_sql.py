import pandas as pd
import sqlite3
import os

# Paths
CSV_FILE = "data/processed/imdb_2024_cleaned.csv"
DB_DIR = "database"
DB_FILE = os.path.join(DB_DIR, "imdb_2024.db")
TABLE_NAME = "movies_2024"

# Ensure database folder exists
os.makedirs(DB_DIR, exist_ok=True)

def load_to_sql():
    # Load CSV
    df = pd.read_csv(CSV_FILE)

    print("Movies loaded from CSV:", df.shape)

    # Connect to SQLite DB
    conn = sqlite3.connect(DB_FILE)

    # Write to SQL
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    conn.close()

    print("✅ Data successfully stored in SQLite database")
    print("📍 Database file:", DB_FILE)
    print("📊 Table name:", TABLE_NAME)

if __name__ == "__main__":
    load_to_sql()
