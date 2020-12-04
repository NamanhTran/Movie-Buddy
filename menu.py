from api.movie_api import get_movie_info

def get_user_genre(genre_set):
    user_genres = []

    while not validate_genres(genre_set, user_genres):

        print("Please choose you favorite genre from the list: (ex: Action, Comedy, Family)")

        for index, genre in enumerate(genre_set):
            print(f"{index + 1}) {genre}")

        user_genres = input("Enter Genre(s): ")
        user_genres = strip_list(user_genres.split(','))
    
    return user_genres

def get_user_movie():
    user_input = None

    while user_input != "y" and user_input != "n":
        user_input = input("(Optional) Would you like to enter movies that you liked in the past to recommend similar movies? (y/n): ")

    if user_input == 'y':
        user_movie = []
        while not validate_movie(user_movie):
            user_movie = input("Enter movie name(s) (ex: La La Land, The Dark Knight, We're the Millers): ")

            user_movie = strip_list(user_movie.split(','))
        
        return user_movie
    
    return None

def get_lowest_acceptable_rating():
    acceptable_rating = -1

    while acceptable_rating < 0 or acceptable_rating > 10:
        user_input = input("On a scale of 0-10, what is the lowest acceptable rating for a movie?: ")

        if not user_input.isnumeric():
            print("Please enter a number")
        
        else:
            acceptable_rating = int(user_input)
    
    return acceptable_rating

def strip_list(string_list):
    stripped_list = []
    for item in string_list:
        stripped_list.append(item.strip())
    
    return stripped_list

def validate_genres(genre_set, genre_list):
    if len(genre_list) == 0:
        return False

    for genre in genre_list:
        if genre not in genre_set:
            print(f"{genre} is not one of the genre option. Please try again or check the spelling.")
            return False
    
    return True

def validate_movie(movie_list):
    if len(movie_list) == 0:
        return False

    for movie in movie_list:
        if get_movie_info(movie) == None:
            return False
    
    return True