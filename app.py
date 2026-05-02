import gradio as gr
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_csv("ex.csv")

# Create user-song matrix
user_song_matrix = data.pivot_table(
    index='user_id',
    columns='song',
    values='rating'
).fillna(0)

# Compute similarity
user_similarity = cosine_similarity(user_song_matrix)

def recommend_songs(user_id):
    user_index = list(user_song_matrix.index).index(int(user_id))
    similarities = user_similarity[user_index]

    similar_users = sorted(
        list(enumerate(similarities)),
        key=lambda x: x[1],
        reverse=True
    )[1:]

    seen_songs = set(
        data[data['user_id'] == int(user_id)]['song']
    )

    recommendations = []

    for sim_user, _ in similar_users:
        songs = data[data['user_id'] == user_song_matrix.index[sim_user]]['song']
        for song in songs:
            if song not in seen_songs and song not in recommendations:
                recommendations.append(song)

            if len(recommendations) == 5:
                return "\n".join(recommendations)

    return "\n".join(recommendations)

demo = gr.Interface(
    fn=recommend_songs,
    inputs=gr.Dropdown(
        choices=list(user_song_matrix.index),
        label="Select User ID"
    ),
    outputs=gr.Textbox(label="Recommended Songs"),
    title="Music Recommendation System"
)

demo.launch()


