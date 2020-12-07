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
        # If the genre has been inserted yet then return since there can be only one 
        # instance of a genre in the graph
        if self.get_node_index(genre) != None:
            return

        # Add the genre to the graph
        self.adjacency_list.append([])

        # Pair the genre name with the index it is located at
        self.node_dictionary[genre.strip()] = self.vertices_count

        # Increase the vertices count for the next genre to be added
        self.vertices_count = self.vertices_count + 1

        return

    # Adds a movie to the graph
    def add_movie(self, movie_data):
        # Create the movie node from the movie data
        movie_node = MovieNode(movie_data)

        # Get the genre related to the movie
        movie_genres = movie_node.genres

        # Add the movie to the genre's adjacency list
        for genre in movie_genres:
            # Get the index location of the genre
            genre_index = self.get_node_index(genre.strip())

            # Add the movie node to the adjacency list
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

    # Perform best first search on the graph
    def best_first_search(self):
        genre_indexes = []

        # Get the genre index for the user's favoirte generes
        for genre in self.favorite_genres:
            genre_indexes.append(self.graph.get_node_index(genre))
        
        # Loops through the genres indexes 
        for genre_index in genre_indexes:
            # Get the list of movies for the genre
            movie_list = self.graph.adjacency_list[genre_index]

            # Loops through the movie list and filters out nodes that to not align with the user's input
            for movie in movie_list:
                # Only consider nodes that meet the min rating, min movie year
                if movie.rating >= self.min_rating and movie.year >= self.min_year:
                    # If the movie node is a repeated node then we increase the weight of the node by 2
                    if movie in self.visited_nodes:
                        # Remove the node from the set
                        self.recommendations_pirority_queue.remove((movie.weight, movie))

                        # Add 2 to the weight of the node
                        movie.weight = movie.weight + 2

                        # Re-add the node back into the set
                        self.recommendations_pirority_queue.add((movie.weight, movie))

                    else:
                        # Calculate the weight of the movie node
                        self.calculate_movie_weight(movie)

                        # Add the node to the pq set
                        self.recommendations_pirority_queue.add((movie.weight, movie))

                        # Add the node to the visted node
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