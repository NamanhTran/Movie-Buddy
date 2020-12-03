import requests, configparser

config = configparser.ConfigParser()
config.read("api_key.cfg")
key = config["API"]["key"]

url = "https://api.themoviedb.org/3/search/movie"
params = {"api_key": key, "query": "This is the end"}

r = requests.get('https://api.themoviedb.org/3/search/movie', params=params)

for movie in r.json()['results']:
    print(movie['original_title'])