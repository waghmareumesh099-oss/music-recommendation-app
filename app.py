import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

auth_manager = SpotifyClientCredentials(client_id=client_id,
                                         client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def recommend_songs(query):
    results = sp.search(q=query, type="track", limit=5)
    
    recommendations = []
    
    for track in results['tracks']['items']:
        artist = track['artists'][0]['name']
        more_tracks = sp.search(q=artist, type="track", limit=5)
        
        for t in more_tracks['tracks']['items']:
            recommendations.append(t['name'] + " - " + t['artists'][0]['name'])
    
    return list(set(recommendations))[:5]

st.title("🎵 Spotify Music Recommendation System")

user_input = st.text_input("Enter song or artist:")

if st.button("Recommend Songs"):
    if user_input:
        songs = recommend_songs(user_input)
        for song in songs:
            st.write("🎶", song)
    else:
        st.write("Please enter something!")
