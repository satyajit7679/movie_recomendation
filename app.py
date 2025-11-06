
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

# Initialize session state for theme
if 'dark_theme' not in st.session_state:
    st.session_state.dark_theme = False

# Custom CSS for both light and dark themes
if st.session_state.dark_theme:
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #0f0f0f;
        color: #ffffff;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        background-color: #6a9ee6;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5a8ed6;
    }
    .movie-card {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #ffffff;
        border-left: 4px solid #6a9ee6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    .title-text {
        font-size: 3rem;
        font-weight: bold;
        color: #6a9ee6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #6a9ee6;
        text-align: center;
        margin: 2rem 0;
    }
    .section-divider {
        height: 2px;
        background-color: #333;
        margin: 2rem 0;
        border: none;
    }
    .footer-text {
        text-align: center;
        color: #999;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    .recommendation-number {
        display: inline-block;
        width: 25px;
        height: 25px;
        background-color: #6a9ee6;
        border-radius: 50%;
        text-align: center;
        line-height: 25px;
        margin-right: 10px;
        font-weight: bold;
        color: white;
        font-size: 0.9rem;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a;
        color: white;
    }
    .stSelectbox div[data-baseweb="select"] input {
        color: white;
    }
    .stSelectbox div[data-baseweb="select"] svg {
        fill: white;
    }
    .stSpinner > div {
        color: #6a9ee6;
    }
    .stAlert {
        background-color: #1a1a1a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        background-color: #4A90E2;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    .movie-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #333;
        border-left: 4px solid #4A90E2;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .title-text {
        font-size: 3rem;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin: 2rem 0;
    }
    .section-divider {
        height: 2px;
        background-color: #e0e0e0;
        margin: 2rem 0;
        border: none;
    }
    .footer-text {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    .recommendation-number {
        display: inline-block;
        width: 25px;
        height: 25px;
        background-color: #4A90E2;
        border-radius: 50%;
        text-align: center;
        line-height: 25px;
        margin-right: 10px;
        font-weight: bold;
        color: white;
        font-size: 0.9rem;
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
    # Theme toggle button at top right
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        theme_label = "🌙 Switch to Dark Theme" if not st.session_state.dark_theme else "☀️ Switch to Light Theme"
        if st.button(theme_label, key="theme_toggle"):
            st.session_state.dark_theme = not st.session_state.dark_theme
            st.rerun()

    # Header
    st.markdown('<p class="title-text">🎬 Movie Recommendation System</p>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

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
                    st.markdown('<p class="recommendation-header">🌟 Recommended Movies For You</p>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    for idx, movie in enumerate(recommendations, 1):
                        st.markdown(
                            f'''
                            <div class="movie-card">
                                <span class="recommendation-number">{idx}</span>
                                <span style="font-size: 1.1rem; font-weight: 600;">{movie}</span>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("No recommendations found. Please try another movie.")

    # Footer
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(
        "<p class='footer-text'>Made with ❤️ using Satyajit Barik</p>",
        unsafe_allow_html=True
    )

else:
    st.error("⚠️ Unable to load movie data. Please check your pickle files.")
    st.info("Make sure 'similarity1.pickle' and 'movie_dict.pickle' are in the same directory as this script.")