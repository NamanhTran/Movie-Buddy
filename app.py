import csv, heapq
from api.movie_api import get_movie_genre, get_movie_info
from menu import get_user_genre, get_user_movie, get_lowest_acceptable_rating, get_earliest_year, display_reccomendation, get_max_list_length

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
        self.visited_nodes = set()
        self.best_first_search()
        self.recommendations_pirority_queue = sorted(self.recommendations_pirority_queue, key=lambda x: x[0], reverse=True)

    def best_first_search(self):
        genre_indexes = []

        for genre in self.favorite_genres:
            genre_indexes.append(self.graph.get_node_index(genre))
        
        for genre_index in genre_indexes:
            movie_list = self.graph.adjacency_list[genre_index]
            for movie in movie_list:
                if movie.rating >= self.min_rating and movie.year >= self.min_year:
                    if movie in self.visited_nodes:
                        self.recommendations_pirority_queue.remove((movie.weight, movie))
                        movie.weight = movie.weight + len(self.favorite_genres)
                        self.recommendations_pirority_queue.add((movie.weight, movie))

                    else:
                        self.calculate_movie_weight(movie)
                        self.recommendations_pirority_queue.add((movie.weight, movie))
                        self.visited_nodes.add(movie)

        return
    
    def calculate_movie_weight(self, movie):
        if movie in self.visited_nodes:
            self.recommendations_pirority_queue.remove((movie.weight, movie))
            movie.weight = movie.weight + len(self.favorite_genres)
            return

        for genre in movie.genres:
            if genre in self.favorite_genres:
                movie.weight = movie.rating

        return

# Opens the data set CSV file and puts 
def create_movie_data(file_location):
    # List of movies dictionaries
    movies_data_list = []

    # Opens the csv file
    with open(file_location, 'r', encoding="utf8") as movies_csv:
        # Create the csv reader object
        csv_reader = csv.reader(movies_csv, delimiter=',')

        # Skip the first row since it just the info header
        next(csv_reader)

        # Go through every movie and take the title, year, genre, description, and rating
        for row in csv_reader:
            # Get the critic reviews so we can filter "indie" movies (most of the time they're not that great)
            critic_reviews = row[21]
            critic_reviews = 0 if critic_reviews == '' else int(critic_reviews)

            # If the movie was released in USA and has more than 20 critic reviews then add it to the list
            if "USA" in set(row[7].split(', ')) and int(critic_reviews) > 20:
                movies_data_list.append({"title": row[2], "year": row[3], "genre": row[5].split(', '), "description": row[13], "rating": row[14]})
    
    return movies_data_list

# Returns a set of genres given a list of movies info
def get_unique_genres(movies_data):
    genre_set = set()

    # Loops through the entire movies list
    for movie_data in movies_data:
        # Loop through all genre in the movie 
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
    
    for movie in movies_data_list:
        movie_graph.add_movie(movie)

    print("Welcome to Movie Buddy!")

    user_genre = get_user_genre(genre_set)

    user_movie = get_user_movie()
    if user_movie != None:
        # for movie in user_movie:
        #     print(get_movie_info(movie)["original_title"])

        for movie in user_movie:
            movie_genre = get_movie_genre(movie)
            if movie_genre != None:
                for genre in movie_genre:
                    if genre not in user_genre and genre != "Documentary" and genre != "TV Movie":
                        user_genre.append(genre)
    
    #print(user_genre)

    acceptable_rating = get_lowest_acceptable_rating()

    earliest_year = get_earliest_year()

    max_length = get_max_list_length()

    best_first_search = MovieBestFirstSearch(movie_graph, user_genre, user_movie, acceptable_rating, earliest_year)

    display_reccomendation(list(best_first_search.recommendations_pirority_queue), max_length)

if __name__ == "__main__":
    main()