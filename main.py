from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('main_data.csv')


# Define a function to create a content-based recommendation system
def recommend_movies(movie_title, data):
    # Create a count vectorizer to convert text data into a matrix of token counts
    count_vectorizer = CountVectorizer(stop_words='english')
    doc_term_matrix = count_vectorizer.fit_transform(data['comb'])

    # Compute the cosine similarity matrix based on the count matrix
    cosine_sim = cosine_similarity(doc_term_matrix)

    # Get the index of the movie that matches the title
    idx = data[data['movie_title'] == movie_title].index[0]

    # Get the pairwise similarity scores between the movie and all other movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar movies
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    # make list of movie titles
    movie_list = data['movie_title'].iloc[movie_indices].to_list()

    return movie_list


# Define a function to get the movie poster URL
def get_movie_url(movie_title):
    api_key = "5a2b803ab1aca7572689acdc80a1f21e"
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    movie_id = response.json()["results"][0]["id"]
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(movie_url)
    poster_url = f"https://image.tmdb.org/t/p/original{response.json()['poster_path']}"

    return poster_url


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the user's input from the form
    movie_title = request.form['movie_title']

    # Call the recommendation function
    recommended_movies = recommend_movies(movie_title, data)

    # Get the URL for the poster of the first recommended movie
    poster_url = get_movie_url(recommended_movies[0])

    # Render the results template with the recommended movies and poster URL
    return render_template('results.html', recommended_movies=recommended_movies, poster_url=poster_url, get_movie_url=get_movie_url)


if __name__ == '__main__':
    app.run(debug=True)
