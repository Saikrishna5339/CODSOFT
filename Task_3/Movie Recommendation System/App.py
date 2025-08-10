import streamlit as st
import pandas as pd
import requests
import pickle
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Recommendation function
def get_recommendations(title, top_n=9):
    if title not in movies['title'].values:
        return pd.DataFrame()
    
    idx = movies[movies['title'] == title].index[0]
    sim_scores = cosine_sim[idx]
    popularity_boost = 1 / (movies['movie_id'] / movies['movie_id'].max() + 1)
    hybrid_scores = 0.7 * sim_scores + 0.3 * popularity_boost
    top_indices = np.argsort(hybrid_scores)[::-1][1:top_n+1]
    
    return movies[['title', 'movie_id']].iloc[top_indices]

# Fetch movie poster
def fetch_poster(movie_id):
    try:
        if not api_key:
            return "https://via.placeholder.com/500x750?text=Missing+API+Key"
        
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        response = requests.get(url)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Streamlit UI Format 3*3 Grid 
st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("Welcome To Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Get Movie Recommendations'):
    recommendations = get_recommendations(selected_movie)
    
    if recommendations.empty:
        st.error("Movie not found!")
    else:
        st.success(f"Movies similar to '{selected_movie}':")
        
        # 3x3 grid layout
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for col, j in zip(cols, range(i, i+3)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    poster_url = fetch_poster(movie_id)
                    
                    with col:
                        st.image(poster_url, width=200)
                        st.write(f"**{movie_title}**")
