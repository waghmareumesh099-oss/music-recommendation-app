import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.title("🎵 Music Recommendation System")

# Load dataset from CSV
data = pd.read_csv("ex(1).csv")

# Create user-song matrix
user_song_matrix = data.pivot_table(
    index='user_id',
    columns='song',
    values='rating'
).fillna(0)

# Compute similarity
user_similarity = cosine_similarity(user_song_matrix)

similarity_df = pd.DataFrame(
    user_similarity,
    index=user_song_matrix.index,
    columns=user_song_matrix.index
)

# Recommendation function
def recommend_songs(user_id, n=5):
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:]

    user_data = user_song_matrix.loc[user_id]
    unseen_songs = user_data[user_data == 0].index

    scores = {}

    for song in unseen_songs:
        score = 0
        for other_user in similar_users.index:
            score += similarity_df[user_id][other_user] * user_song_matrix.loc[other_user][song]
        scores[song] = score

    recommended = sorted(scores, key=scores.get, reverse=True)
    return recommended[:n]

selected_user = st.selectbox(
    "Select User ID",
    user_song_matrix.index
)

if st.button("Recommend Songs"):
    recommendations = recommend_songs(selected_user)

    st.subheader("Recommended Songs:")
    for song in recommendations:
        st.write("🎶", song)
