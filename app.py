import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="IMDb 2024 Movies Dashboard", layout="wide")
st.title("🎬 IMDb 2024 Movies Analysis Dashboard")

DB_PATH = "database/imdb_2024.db"

@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        st.error(f"Database not found: {DB_PATH}")
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()

    return df


df = load_data()

# 🚨 SAFETY CHECK (VERY IMPORTANT)
if df.empty:
    st.stop()

# ───────────────── Sidebar Filters ─────────────────
st.sidebar.header("🎛 Filter Movies")

all_genres = sorted(
    set(
        g.strip()
        for genres in df["genre"].dropna().str.split(",")
        for g in genres
    )
)

selected_genres = st.sidebar.multiselect(
    "Select Genre", all_genres, default=all_genres
)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)
min_votes = st.sidebar.number_input("Minimum Votes", min_value=0, value=1000, step=1000)
min_duration, max_duration = st.sidebar.slider("Duration (minutes)", 0, 300, (60, 180))

filtered_df = df[
    (df["rating"] >= min_rating) &
    (df["votes"] >= min_votes) &
    (df["duration_minutes"].between(min_duration, max_duration))
]

filtered_df = filtered_df[
    filtered_df["genre"].apply(
        lambda x: any(g in x for g in selected_genres) if isinstance(x, str) else False
    )
]

# ───────────────── Metrics ─────────────────
col1, col2, col3 = st.columns(3)
col1.metric("🎥 Total Movies", len(filtered_df))
col2.metric("⭐ Average Rating", round(filtered_df["rating"].mean(), 2))
col3.metric("⏱ Avg Duration", round(filtered_df["duration_minutes"].mean(), 1))

# ───────────────── Charts ─────────────────
st.subheader("🏆 Top 10 Movies")
st.dataframe(
    filtered_df.sort_values("rating", ascending=False).head(10),
    use_container_width=True
)

st.subheader("🎭 Genre Distribution")
genre_df = filtered_df.assign(
    genre=filtered_df["genre"].str.split(",")
).explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()

fig1, ax1 = plt.subplots()
genre_df["genre"].value_counts().head(10).plot(kind="bar", ax=ax1)
st.pyplot(fig1)

st.subheader("⭐ Rating Distribution")
fig2, ax2 = plt.subplots()
ax2.hist(filtered_df["rating"].dropna(), bins=20)
st.pyplot(fig2)

st.subheader("📈 Rating vs Votes")
fig3, ax3 = plt.subplots()
ax3.scatter(filtered_df["votes"], filtered_df["rating"], alpha=0.5)
st.pyplot(fig3)
