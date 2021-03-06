import requests, configparser, os

def get_movie_genre(movie_name):
    movie_genre = []
    movie_info = get_movie_info(movie_name)
    movie_genre_ids = movie_info["genre_ids"]

    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": get_api_key(os.path.join(os.path.dirname(__file__), 'api_key.cfg'))}

    r = requests.get(url, params=params)
    all_genre_list = r.json()["genres"]
    all_genre_id_dict = {}

    for genre in all_genre_list:
        all_genre_id_dict[genre["id"]] = genre["name"]
    
    for genre_id in movie_genre_ids:
        movie_genre.append(all_genre_id_dict[genre_id])
    
    return movie_genre

# Returns movie information gathered from the TMDb's search API
def get_movie_info(movie_name):
    # Get the API key from the cfg file
    key = get_api_key(os.path.join(os.path.dirname(__file__), 'api_key.cfg'))

    # Location of the API endpoint
    url = "https://api.themoviedb.org/3/search/movie"

    # Set the parameters for our API key and the query term 
    params = {"api_key": key, "query": movie_name}

    # Execute the get request to the API
    r = requests.get(url, params=params)

    # Extract the results from the response
    movies = r.json()['results']

    # If there are no matching movies return None
    if len(movies) == 0:
        return None
    
    # Return the first relavent movie result in the results
    return movies[0]

def get_api_key(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config["API"]["key"]