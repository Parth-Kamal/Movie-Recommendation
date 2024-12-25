import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch the poster of a movie using The Movie Database API
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies based on the selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))  # Fetch poster from API
    return recommended_movie, recommended_movie_poster

# Load the movie dictionary and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title and description
st.set_page_config(page_title="Movie Recommender", layout="wide", page_icon="🎥")
st.title('🎥 Movie Recommender System')
st.markdown(
    """
    <style>
    body {background-color: #f5f5f5;}
    .movie-container:hover {transform: scale(1.05); transition: 0.3s;}
    .movie-title {font-size: 16px; font-weight: bold; text-align: center;}
    .movie-poster {border-radius: 8px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    **Welcome to the Movie Recommender System!**  
    Simply select a movie you like, and we will recommend five similar movies.  
    Enjoy discovering new movies tailored to your taste!  
    """,
    unsafe_allow_html=True,
)

# Dropdown menu for selecting a movie
selected_movies = st.selectbox(
    "Search for a movie:",
    movies['title'].values
)

# Button to get recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movies)

    st.markdown("---")
    st.subheader("Recommendations")
    st.markdown("Here are some movies you might like:")

    # Display recommended movies and posters in a responsive grid layout
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], caption=names[idx], use_container_width=True)  # Updated parameter
            st.markdown(
                f"<div class='movie-title'>{names[idx]}</div>",
                unsafe_allow_html=True,
            )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: grey;">
        Developed with ❤️ by Parth Kamal | Powered by <a href="https://www.themoviedb.org/" target="_blank">TMDB API</a>
    </div>
    """,
    unsafe_allow_html=True
)

