import gradio as gr
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_csv("ex.csv")

# Clean rating column
data["User-Rating"] = data["User-Rating"].str.replace("/10", "").astype(float)

# Combine features
data["combined_features"] = (
    data["Genre"] + " " +
    data["Singer/Artists"] + " " +
    data["Album/Movie"]
)

# Vectorize text
vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform(data["combined_features"])

# Similarity matrix
similarity = cosine_similarity(feature_matrix)

# Recommendation function
def recommend(song_name):
    if song_name not in data["Song-Name"].values:
        return "Song not found in dataset."

    idx = data[data["Song-Name"] == song_name].index[0]

    similar_songs = list(enumerate(similarity[idx]))
    sorted_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []

    for i in sorted_songs:
        recommendations.append(data.iloc[i[0]]["Song-Name"])

    return "\n".join(recommendations)

# Gradio Interface
demo = gr.Interface(
    fn=recommend,
    inputs=gr.Dropdown(
        choices=sorted(data["Song-Name"].unique().tolist()),
        label="Select Song"
    ),
    outputs=gr.Textbox(label="Recommended Songs"),
    title="Music Recommendation System"
)

demo.launch()
