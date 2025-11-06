
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better design
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title-text {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load movie data and similarity matrix"""
    try:
        similarity = pickle.load(open('similarity1.pickle', 'rb'))

        # Convert to numpy array if needed
        if isinstance(similarity, pd.DataFrame):
            similarity = similarity.values

        with open('movie_dict.pickle', 'rb') as f:
            movies_dict = pickle.load(f)

        movies = pd.DataFrame(movies_dict)
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None




def recommend(movie, movies, similarity):
    """Get movie recommendations"""
    try:
        # Find the index of the selected movie
        movie_index = movies[movies['title'] == movie].index[0]

        # Get similarity scores - this should be a row from similarity matrix
        distance = similarity[movie_index]

        # Convert to list if it's an array
        if hasattr(distance, 'tolist'):
            distance = distance.tolist()

        # Clean the data - ensure all values are numeric
        cleaned_distance = []
        for val in distance:
            try:
                # Try to convert to float
                cleaned_distance.append(float(val))
            except (ValueError, TypeError):
                # If conversion fails, use 0 as similarity score
                cleaned_distance.append(0.0)

        # Sort and get top 5 recommendations
        movies_list = sorted(
            list(enumerate(cleaned_distance)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        recommended_movies = []
        for i in movies_list:

            recommended_movies.append(movies.iloc[i[0]].title)

        return recommended_movies

    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []


# Load data
movies, similarity = load_data()

if movies is not None and similarity is not None:
    # Header
    st.markdown('<p class="title-text">🎬 Movie Recommendation System</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Main layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🎯 Select Your Favorite Movie")
        selected_movie_name = st.selectbox(
            "Choose a movie you enjoyed:",
            movies['title'].values,
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Buttons
        button_col1, button_col2 = st.columns(2)

        with button_col1:
            recommend_button = st.button("🎬 Get Recommendations", type="primary")

        with button_col2:
            reset_button = st.button("🔄 Reset")

        # Handle reset
        if reset_button:
            st.rerun()

        # Handle recommendations
        if recommend_button:
            with st.spinner("Finding perfect movies for you..."):
                recommendations = recommend(selected_movie_name, movies, similarity)

                if recommendations:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 🌟 Recommended Movies For You")
                    st.markdown("<br>", unsafe_allow_html=True)

                    for idx, movie in enumerate(recommendations, 1):
                        st.markdown(
                            f'<div class="movie-card">🎥 {idx}. {movie}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("No recommendations found. Please try another movie.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ using Satyajit</p>",
        unsafe_allow_html=True
    )

else:
    st.error("⚠️ Unable to load movie data. Please check your pickle files.")
    st.info("Make sure 'similarity.pickle' and 'movie_dict.pickle' are in the same directory as this script.")
