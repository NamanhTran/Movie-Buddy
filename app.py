import csv, heapq
from api.movie_api import get_movie_genre, get_movie_info
from menu import get_user_genre, get_user_movie, get_lowest_acceptable_rating, get_earliest_year

# Node that holds all relavent information about the movie
class MovieNode:
    def __init__(self, movie_data):
        self.title = movie_data["title"]
        self.year = int(movie_data["year"])
        self.genres = movie_data["genre"]
        self.description = movie_data["description"]
        self.rating = float(movie_data["rating"])
        self.weight = 0

# A Bipartite Graph that is implemented using adjacency lists
class MovieAdjacencyBipartiteGraph:
    # Constructor
    def __init__(self):
        # Adjacency list that it's index represents a node and its list hold its neighbors
        self.adjacency_list = []

        # A dictionary is used to figure out the index of a node
        self.node_dictionary = {}

        # Amount of vertices in the graph
        self.vertices_count = 0
    
    # Adds genre to the graph
    def add_genre(self, genre):
        if self.get_node_index(genre) == None:
            self.adjacency_list.append([])

        self.node_dictionary[genre.strip()] = self.vertices_count
        self.vertices_count = self.vertices_count + 1

    # Adds a movie to the graph
    def add_movie(self, movie_data):
        movie_node = MovieNode(movie_data)
        movie_genres = movie_node.genres

        for genre in movie_genres:
            genre_index = self.get_node_index(genre.strip())
            self.adjacency_list[genre_index].append(movie_node)

        return
    
    def get_node_index(self, key):
        index = self.node_dictionary.get(key)
        if index != None:
            return index
        
        return None

class MovieBestFirstSearch:
    def __init__(self, graph, genres, movies, min_rating, min_year):
        self.graph = graph
        self.favorite_genres = genres
        self.movies = movies
        self.min_rating = min_rating
        self.recommendations_pirority_queue = set()
        self.min_year = min_year
        self.best_first_search()
        self.recommendations_pirority_queue = sorted(self.recommendations_pirority_queue, key=lambda x: x[0], reverse=True)
        #print(self.recommendations_pirority_queue)

    def best_first_search(self):
        genre_indexes = []
        visited_nodes = set()

        for genre in self.favorite_genres:
            genre_indexes.append(self.graph.get_node_index(genre))
        
        for genre_index in genre_indexes:
            movie_list = self.graph.adjacency_list[genre_index]
            for movie in movie_list:
                if movie.rating >= self.min_rating and movie.year >= self.min_year:
                    if movie.title in visited_nodes:
                        # TODO Increase the weight of the node by 1 since it shares two genres that the user liked
                        self.recommendations_pirority_queue.remove((movie.weight, movie))
                        movie.weight = movie.weight + 1
                        self.recommendations_pirority_queue.add((movie.weight, movie))
                        print(movie, movie.weight)
                        #print(f"Need to increase weight of {movie.title}")

                    else:
                        self.calculate_movie_weight(movie)
                        self.recommendations_pirority_queue.add((movie.weight, movie))
                        visited_nodes.add(movie.title)
                        print(movie.title, movie.weight, movie.rating, movie.genres, self.favorite_genres)

        return
    
    def calculate_movie_weight(self, movie):
        for genre in movie.genres:
            if genre in self.favorite_genres:
                movie.weight = movie.rating

        return -1

def create_movie_data(file_location):
    movies_data_list = []

    with open(file_location, 'r', encoding="utf8") as movies_csv:
        csv_reader = csv.reader(movies_csv, delimiter=',')
        next(csv_reader)

        for movie in csv_reader:
            critic_reviews = movie[21]
            critic_reviews = 0 if critic_reviews == '' else int(critic_reviews)

            if "USA" in set(movie[7].split(', ')) and int(critic_reviews) > 20:
                movies_data_list.append({"title": movie[2], "year": movie[3], "genre": movie[5].split(', '), "description": movie[13], "rating": movie[14]})
    
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

    movie_graph = MovieAdjacencyBipartiteGraph()

    for genre in genre_set:
        movie_graph.add_genre(genre)

    #print(movie_graph.node_dictionary)
    
    for movie in movies_data_list:
        movie_graph.add_movie(movie)

    #print(genre_set)

    print("Welcome to Movie Buddy!")

    user_genre = get_user_genre(genre_set)
    #print(user_genre)

    user_movie = get_user_movie()
    if user_movie != None:
        # for movie in user_movie:
        #     print(get_movie_info(movie)["original_title"])

        for movie in user_movie:
            movie_genre = get_movie_genre(movie)
            if movie_genre != None:
                for genre in movie_genre:
                    if genre not in user_genre:
                        user_genre.append(genre)
    
    #print(user_genre)

    acceptable_rating = get_lowest_acceptable_rating()
    #print(acceptable_rating)

    earliest_year = get_earliest_year()
    #print(earliest_year)

    best_first_search = MovieBestFirstSearch(movie_graph, user_genre, user_movie, acceptable_rating, earliest_year)

    for i in range(75):
        print(list(best_first_search.recommendations_pirority_queue)[i][1].title)

if __name__ == "__main__":
    main()