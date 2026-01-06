import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="IMDb 2024 Movies Dashboard", layout="wide")

st.title("🎬 IMDb 2024 Movies Analysis Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/imdb_2024_cleaned.csv")

df = load_data()

st.sidebar.header("🎛 Filter Movies")

# Genre filter
all_genres = sorted(
    set(g.strip() for genres in df["genre"].dropna().str.split(",") for g in genres)
)
selected_genres = st.sidebar.multiselect(
    "Select Genre", all_genres, default=all_genres
)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating", 0.0, 10.0, 5.0, 0.1
)

# Votes filter
min_votes = st.sidebar.number_input(
    "Minimum Votes", min_value=0, value=1000, step=1000
)

# Duration filter
min_duration, max_duration = st.sidebar.slider(
    "Duration (minutes)", 0, 300, (60, 180)
)
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

col1, col2, col3 = st.columns(3)

col1.metric("🎥 Total Movies", len(filtered_df))
col2.metric("⭐ Average Rating", round(filtered_df["rating"].mean(), 2))
col3.metric("⏱ Avg Duration (min)", round(filtered_df["duration_minutes"].mean(), 1))

st.subheader("🏆 Top 10 Movies by Rating")

top_movies = (
    filtered_df.sort_values(by="rating", ascending=False)
    .head(10)[["movie_name", "genre", "rating", "votes", "duration_minutes"]]
)

st.dataframe(top_movies, use_container_width=True)

st.subheader("🎭 Genre Distribution")

genre_df = filtered_df.copy()
genre_df["genre"] = genre_df["genre"].str.split(",")
genre_df = genre_df.explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()

genre_counts = genre_df["genre"].value_counts().head(10)

fig1, ax1 = plt.subplots()
genre_counts.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Movie Count")
ax1.set_title("Top 10 Genres")
st.pyplot(fig1)

st.subheader("⏱ Average Duration by Genre")

avg_duration = (
    genre_df.groupby("genre")["duration_minutes"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
avg_duration.plot(kind="barh", ax=ax2)
ax2.set_xlabel("Duration (minutes)")
ax2.set_title("Average Duration by Genre")
st.pyplot(fig2)

st.subheader("⭐ Rating Distribution")

fig3, ax3 = plt.subplots()
ax3.hist(filtered_df["rating"].dropna(), bins=20)
ax3.set_xlabel("Rating")
ax3.set_ylabel("Count")
st.pyplot(fig3)

st.subheader("📈 Rating vs Votes")

fig4, ax4 = plt.subplots()
ax4.scatter(filtered_df["votes"], filtered_df["rating"], alpha=0.5)
ax4.set_xlabel("Votes")
ax4.set_ylabel("Rating")
st.pyplot(fig4)

st.subheader("📋 Filtered Movie List")
st.dataframe(filtered_df, use_container_width=True)
