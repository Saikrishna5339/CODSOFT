import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load datasets
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')


movies = movies.merge(credits, on='title')

# Keep only relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
def convert(obj):
    I = []
    for i in ast.literal_eval(obj):
        I.append(i['name'])
    return I

# For conversions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Keep top 3 actors in cast
movies['cast'] = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)[:3]])

# Extract director from crew
movies['crew'] = movies['crew'].apply(lambda x: [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director'])

# Combine all tags
movies['tags'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Convert list of tags to string
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

# Keep only final useful columns
movies = movies[['movie_id', 'title', 'overview', 'tags']]

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['tags'])

# Cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# MODIFIED RECOMMENDATION SYSTEM - Using Hybrid and Similarity Score 
def get_recommendations(title, top_n=10):
    if title not in movies['title'].values:
        return f"Movie '{title}' not found in dataset."
    idx = movies[movies['title'] == title].index[0]
    
    sim_scores = cosine_sim[idx]
   
    popularity_boost = 1 / (movies['movie_id'] / movies['movie_id'].max() + 1)
   
    hybrid_scores = 0.7 * sim_scores + 0.3 * popularity_boost
    top_indices = np.argsort(hybrid_scores)[::-1][1:top_n+1]
    return movies['title'].iloc[top_indices].values


print(get_recommendations('The Dark Knight Rises'))

# Saves model data for future use
with open('movie_data.pkl', 'wb') as file:
    pickle.dump((movies, cosine_sim), file)