import requests, configparser, os

def get_movie_genre(movie_name):
    movie_genre = []
    movie_info = get_movie_info(movie_name)
    movie_genre_ids = movie_info["genre_ids"]

    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": get_api_key("api_key.cfg")}

    r = requests.get(url, params=params)
    all_genre_list = r.json()["genres"]
    all_genre_id_dict = {}

    for genre in all_genre_list:
        all_genre_id_dict[genre["id"]] = genre["name"]
    
    for genre_id in movie_genre_ids:
        movie_genre.append(all_genre_id_dict[genre_id])
    
    return movie_genre

# Grabs the first most relevant result even if there are other matches
def get_movie_info(movie_name):
    key = get_api_key(os.path.join(os.path.dirname(__file__), 'api_key.cfg'))

    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": key, "query": movie_name}

    r = requests.get(url, params=params)
    movies = r.json()['results']

    if len(movies) == 0:
        return None

    print(movies[0]["original_title"])
    
    return movies[0]

def get_api_key(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config["API"]["key"]