import sqlite3
import pandas as pd

conn = sqlite3.connect("database/imdb_2024.db")

query1 = "SELECT COUNT(*) AS total_movies FROM movies_2024;"
print(pd.read_sql(query1, conn))


query2 = """
SELECT movie_name, genre, rating, votes
FROM movies_2024
WHERE votes > 10000
ORDER BY rating DESC
LIMIT 10;
"""
print(pd.read_sql(query2, conn))


query3 = """
SELECT AVG(rating) AS avg_rating
FROM movies_2024
WHERE genre LIKE '%Drama%';
"""
print(pd.read_sql(query3, conn))

conn.close()
