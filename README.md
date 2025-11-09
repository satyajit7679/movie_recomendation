🎬 Movie Recommendation App

A simple Streamlit-based movie recommender that suggests top-5 similar movies using a precomputed similarity model.

🚀 Features

Select a movie → get 5 similar movies

Fast (pre-computed similarity)

Minimal & easy to run

📂 Project Structure
movie_recomendation/
│── app.py                 # Main Streamlit app
│── main.ipynb             # Notebook used to create pickle files
│── movie_dict.pickle      # Movie metadata stored as dict
│── movie.pickle           # Movie data used in app
│── similarity1.pickle     # Precomputed similarity matrix
│── tmdb_5000_movies.csv   # Dataset
│── tmdb_5000_credits.csv  # Dataset
│── requirements.txt       # Dependencies
│── templete/              # (Optional) template folder
└── .devcontainer/         # Dev environment setup

⚙️ How It Works

Movie data is preprocessed in main.ipynb

A similarity matrix is generated using text features (genres, cast, crew, overview)

app.py loads the matrix + movie data and returns top recommendations

🏁 Run Locally
1️⃣ Clone
git clone https://github.com/satyajit7679/movie_recomendation.git
cd movie_recomendation

2️⃣ Install
pip install -r requirements.txt

3️⃣ Run
streamlit run app.py


🔗 Live Demo:
👉 https://mymovierecomendation.streamlit.app/
