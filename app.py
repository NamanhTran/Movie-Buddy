import csv
from api.movie_api import get_movie_genre, get_movie_info
from menu import get_user_genre, get_user_movie, get_lowest_acceptable_rating

class GenreNode:
    def __init__(self, genre):
        self.genre = genre
        self.neighbors = []
    
    def add_neighbors(self, node):
        self.neighbors.append(node)

class MovieNode:
    def __init__(self, movie_info):
        self.title = movie_info["title"]
        self.movie_info = movie_info

class MovieAdjacencyBipartitieGraph:
    def __init__(self, genre_set):
        self.adjacency_list = []
        self.genre_index = {}
        self.vertices_count = 0
    
    def add_genre(self, genre):
        self.adjacency_list.append(self.vertices_count)
        self.genre_index[genre] = self.vertices_count
        self.vertices_count = self.vertices_count + 1

    def add_movie(self, movie_data):
        # Find out which genre it is first then add it as a neighbor to the genre node
        raise NotImplementedError
    
    def get_genre_index(self, genre):
        index = self.genre_index.get(genre)
        if index != None:
            return index
        
        return None

class MovieBestFirstSearch:
    def __init__(self):
        raise NotImplementedError

def create_movie_data(file_location):
    movies_data_list = []

    with open(file_location, 'r', encoding="utf8") as movies_csv:
        csv_reader = csv.reader(movies_csv, delimiter=',')
        next(csv_reader)

        for movie in csv_reader:
            movies_data_list.append({"title": movie[1], "year": movie[3], "genre": movie[5].split(','), "description": movie[13], "rating": movie[14]})
    
    return movies_data_list

def get_unique_genres(movies_data):
    genre_set = set()

    for movie_data in movies_data:
        for genre in movie_data["genre"]:
            if genre not in genre_set:
                genre_set.add(genre.strip())
    
    return genre_set

def main():
    movies_data_dict = create_movie_data("./datasets/movies.csv")
    genre_set = get_unique_genres(movies_data_dict)

    print(genre_set)

    print("Welcome to Movie Buddy!")

    user_genre = get_user_genre(genre_set)
    print(user_genre)

    user_movie = get_user_movie()
    print(user_movie)

    acceptable_rating = get_lowest_acceptable_rating()
    print(acceptable_rating)

if __name__ == "__main__":
    main()