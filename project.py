import csv

class MovieBipartitieGraph:
    def __init__():


def create_movie_data(file_location):
    movies_data_list = []

    with open(file_location, 'r', encoding="utf8") as movies_csv:
        movies = csv.reader(movies_csv, delimiter=',')

        for movie in movies:
            movies_data_list.append({"title": movie[1], "year": movie[3], "genre": movie[5].split(','), "description": movie[13], "rating": movie[14]})
    
    return movies_data_list

def get_unique_genres(movies_data):
    genre_set = set()

    for movie_data in movies_data:
        for genre in movie_data["genre"]:
            if genre not in genre_set:
                genre_set.add(genre)
    
    return genre_set

def main():
    movies_data_dict = create_movie_data("./movies.csv")
    genre_set = get_unique_genres(movies_data_dict)

    print(genre_set)

if __name__ == "__main__":
    main()