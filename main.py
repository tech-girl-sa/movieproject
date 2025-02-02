import random
import matplotlib.pyplot as plt
from thefuzz import process
from movie_storage import (add_movie, list_movies,
                           delete_movie, update_movie)


def input_rating(prompt_message="Enter the movie's rating: ", allow_blank = False):
    while True:
        rating = input(prompt_message)
        if allow_blank and not rating:
            return 0
        try:
            rating = float(rating)
            if not 0 <= rating <= 10:
                raise ValueError("rating should be between 0 and 10")
            return rating
        except ValueError:
            print(f"Rating {rating} is not valid.")


def input_year(prompt_message="Enter the movie's year: ",allow_blank = False):
    while True:
        year = input(prompt_message)
        if allow_blank and not year:
            return year
        try:
            year = int(year)
            return year
        except ValueError:
            print(f"Year {year} is not valid.")


def new_movie():
    movies = list_movies()
    movie = ""
    while not movie or movie in movies:
        movie = input("Enter the movie's name: ")
        if movie in movies:
            print(f"Movie {movie} already exists")
        if not movie:
            print(f"Please enter a valid film name")
    rating = input_rating()
    year = input_year()
    add_movie(movie, year, rating)
    print("Movie added successfully")


def get_movies():
    movies = list_movies()
    print(f"{len(movies.keys())} movies in total")
    for movie in movies:
        print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")

def get_fuzz_suggestions(movie,movies):
    list_movies = list(movies.keys())
    suggestions=process.extract(movie,list_movies)
    accurate_suggestions = [suggestion for suggestion in suggestions if suggestion[1] >= 73]
    return accurate_suggestions

def remove_movie():
    movies = list_movies()
    movie = input("Enter Movie name to delete: ")
    if movie in movies:
        delete_movie(movie)
        print(f"Movie {movie} deleted successfully!")
    else:
        suggestions= get_fuzz_suggestions(movie,movies)
        print(f"Movie {movie} doesn't exist!")
        if suggestions:
            print(f"did you mean {suggestions[0][0]}")


def edit_movie():
    movies = list_movies()
    movie = input("Enter the movie's name: ")
    if movie not in movies:
        suggestions = get_fuzz_suggestions(movie, movies)
        print(f"Movie {movie} doesn't exist!")
        if suggestions:
            print(f"did you mean {suggestions[0][0]}")
        return
    rating = input_rating()
    update_movie(movie, rating)
    print("Movie is updated successfully!")



def get_average(ratings):
    return round(sum(ratings) / len(ratings),1)


def get_median(ratings):
    ratings.sort()
    if len(ratings) % 2 == 0:
        half = len(ratings) // 2
        return round((ratings[half - 1] + ratings[half]) / 2,1)
    else:
        half = len(ratings) // 2
        return ratings[half]


def get_movies_based_on_rating(rating, movies):
    list_movies = [(movie, movies[movie]["rating"]) for movie in movies
                   if rating == movies[movie]["rating"]]
    return list_movies


def get_best_movies(movies):
    ratings = [movies[movie]["rating"] for movie in movies]
    ratings.sort(reverse=True)
    best_rating = ratings[0]
    return get_movies_based_on_rating(best_rating, movies)


def get_worst_movies(movies):
    ratings = [movies[movie]["rating"] for movie in movies]
    ratings.sort()
    worst_rating = ratings[0]
    return get_movies_based_on_rating(worst_rating, movies)


def stats():
    movies = list_movies()
    ratings = [movies[movie]["rating"] for movie in movies]
    average = get_average(ratings)
    median = get_median(ratings)
    best_movies = "; ".join([f"{movie}, {rating}" for movie, rating in get_best_movies(movies)])
    worst_movies = "; ".join([f"{movie}, {rating}" for movie, rating in get_worst_movies(movies)])
    print(f"Average rating: {average}")
    print(f"Median rating: {median}")
    print(f"Best movie: {best_movies}")
    print(f"Worst movie: {worst_movies}")


def random_movie():
    movies = list_movies()
    random_movie = random.choice(list(movies.keys()))
    print(f"Your movie tonight: {random_movie}, it's rated {movies[random_movie]['rating']}")


def search_movie():
    movies = list_movies()
    searched_movie = input("Enter part of movie: ")
    no_movie=True
    for movie in movies:
        if searched_movie.lower() in movie.lower():
            no_movie=False
            print(f"{movie}, {movies[movie]['rating']}")
    if no_movie:
        print(f"{searched_movie} doesn't exist!")
        suggestions=get_fuzz_suggestions(searched_movie,movies)
        if suggestions:
            print("Did you mean?")
        for suggestion in suggestions:
            print(suggestion[0])


def sort_movies():
    movies = list_movies()
    ratings = [movies[movie]["rating"] for movie in movies]
    ratings.sort(reverse=True)
    for rating in ratings:
        for movie in get_movies_based_on_rating(rating, movies):
            print(f"{movie[0]}: {movie[1]}")

def get_histogram():
    movies = list_movies()
    ratings = [movies[movie]["rating"] for movie in movies]
    file_name=input("Enter the name of file you want to save to: ")
    plt.hist(ratings)
    plt.xlabel('Ratings', fontweight='bold', horizontalalignment='center')
    plt.ylabel('Number Of Films',fontweight='bold')
    plt.title("Distribution Of Ratings", fontweight='bold', color='blue', fontsize='14')
    plt.savefig(f"{file_name}.png")


def exit():
    print("Bye!")


def filter_movies():
    minimum_rating = input_rating("Enter minimum rating (leave blank for no minimum rating): ", allow_blank=True)
    start_year = input_year("Enter start year (leave blank for no start year): ", allow_blank=True)
    end_year = input_year("Enter end year (leave blank for no end year): ", allow_blank= True)
    if not start_year:
        start_year = -3000
    if not end_year:
        end_year = 3000
    if end_year < start_year:
        end_year, start_year = start_year, end_year
    movies = list_movies()
    filtered_movies = [(movie,movies[movie]["rating"],movies[movie]["year"]) for movie in movies
                       if (movies[movie]["rating"]>= minimum_rating and
                           start_year<=movies[movie]["year"]<=end_year)]
    for movie, rating, year in filtered_movies:
        print(f"{movie} ({rating}): {year}")



def main():
    print("********** My Movies Database **********")
    print("\t" * 3)
    while True:
        print("""Menu:
0.  Exit
1.  List movies
2.  Add movie
3.  Delete movie
4.  Update movie
5.  Stats
6.  Random movie
7.  Search movie
8.  Movies sorted by rating
9.  Create Rating Histogram
10. Filter Movies
      """)
        user_input = input("Enter choice (0-10): ")
        print("\t" * 2)
        if not user_input.isnumeric() or int(user_input) not in range(11):
            print("Invalid Choice")
            continue
        functions_mapping = {
            "0": exit,
            "1": get_movies,
            "2": new_movie,
            "3": remove_movie,
            "4": edit_movie,
            "5": stats,
            "6": random_movie,
            "7": search_movie,
            "8": sort_movies,
            "9": get_histogram,
            "10": filter_movies
        }
        functions_mapping[user_input]()
        if user_input == "0":
            break
        print("\t" * 2)
        input("Press enter to continue ")
        print("\t" * 2)



if __name__ == "__main__":
    main()