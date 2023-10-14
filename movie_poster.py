import requests

API_KEY = "5a2b803ab1aca7572689acdc80a1f21e"

def get_movie_poster(title):
    # Make a request to the TMDB API to search for the movie
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(search_url)

    # Parse the response JSON to get the movie ID
    movie_id = response.json()["results"][0]["id"]

    # Make a request to the TMDB API to get information about the movie
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(movie_url)

    # Return the URL of the poster image
    return f"https://image.tmdb.org/t/p/original{response.json()['poster_path']}"