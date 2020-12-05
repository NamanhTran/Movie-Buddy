import csv, heapq
from api.movie_api import get_movie_genre, get_movie_info
from menu import get_user_genre, get_user_movie, get_lowest_acceptable_rating

class MovieAdjacencyBipartitieGraph:
    def __init__(self):
        self.adjacency_list = []
        self.node_dictionary = {}
        self.index_dictionary = {}
        self.vertices_count = 0
    
    # TODO: Need to push a list instead of the number
    def add_genre(self, genre):
        if self.get_node_index(genre) == None:
            self.adjacency_list.append([])

        self.node_dictionary[genre.strip()] = self.vertices_count
        self.vertices_count = self.vertices_count + 1

    def add_movie(self, movie_data):
        movie_genres = movie_data["genre"]

        for genre in movie_genres:
            genre_index = self.get_node_index(genre.strip())
            self.adjacency_list[genre_index].append(movie_data)

        return
    
    def get_node_index(self, key):
        index = self.node_dictionary.get(key)
        if index != None:
            return index
        
        return None

class MovieBestFirstSearch:
    def __init__(self, graph, genres):
        self.graph = graph
        self.genres = genres
        self.recommendations_queue = []
        self.search()

    def search():
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
    movies_data_list = create_movie_data("./datasets/movies.csv")
    genre_set = get_unique_genres(movies_data_list)

    movie_graph = MovieAdjacencyBipartitieGraph()

    for genre in genre_set:
        movie_graph.add_genre(genre)

    print(movie_graph.node_dictionary)
    
    for movie in movies_data_list:
        movie_graph.add_movie(movie)

    #print(movie_graph.adjacency_list[4])

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