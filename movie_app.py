import random
import matplotlib.pyplot as plt

from omdb_api import OMDbApi, OMDbApiException
from outils import input_rating, input_year, get_fuzz_suggestions, get_average, get_median, get_best_movies, \
    get_worst_movies, get_movies_based_on_rating, input_data_manual_entry, generate_html_elements


class MovieApp:

    def __init__(self, storage):
        self._storage = storage
        self._functions_mapping =  {
            "0": self._exit,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_movies_sorted_by_rating,
            "9": self._command_create_rating_histogram,
            "10": self._command_filter_movies,
            "11": self._generate_website
        }
        self._menu = """    Menu:
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
    11. Generate Website
      """


    def _command_list_movies(self):
        """Lists all movies"""
        movies = self._storage.list_movies()
        print(f"{len(movies.keys())} movies in total")
        for movie in movies:
            print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


    def _command_add_movie(self):
        """Adds a new movie if it doesn't exist already with proper input validation"""
        movies = self._storage.list_movies()
        movie = ""
        while not movie or movie in movies:
            movie = input("Enter the movie's name: ")
            if movie in movies:
                print(f"Movie {movie} already exists")
            if not movie:
                print(f"Please enter a valid film name")
        poster = ""
        try:
            movie_info = OMDbApi.get_movie(movie)
            rating = movie_info["rating"]
            year = movie_info["year"]
            poster = movie_info["poster"]
        except OMDbApiException as e:
            print(e)
            user_input = input_data_manual_entry()
            if user_input == "y":
                rating = input_rating()
                year = input_year()
            else:
                return
        self._storage.add_movie(movie, year, rating, poster)
        print("Movie added successfully")


    def _command_delete_movie(self):
        """Deletes entered movie if it exists with auto correct support in case of typo in name of the film"""
        movies = self._storage.list_movies()
        movie = input("Enter Movie name to delete: ")
        if movie in movies:
            self._storage.delete_movie(movie)
            print(f"Movie {movie} deleted successfully!")
        else:
            suggestions = get_fuzz_suggestions(movie, movies)
            print(f"Movie {movie} doesn't exist!")
            if suggestions:
                print(f"did you mean {suggestions[0][0]}")


    def _command_update_movie(self):
        """Updates entered movie if it exists with auto correct support in case of typo in name of the film"""
        movies = self._storage.list_movies()
        movie = input("Enter the movie's name: ")
        if movie not in movies:
            suggestions = get_fuzz_suggestions(movie, movies)
            print(f"Movie {movie} doesn't exist!")
            if suggestions:
                print(f"did you mean {suggestions[0][0]}")
            return
        rating = input_rating()
        self._storage.update_movie(movie, rating)
        print("Movie is updated successfully!")


    def _command_movie_stats(self):
        """Displays average ratings, Median of the ratings, Best rated movie and Worst rated movie"""
        movies = self._storage.list_movies()
        ratings = [movies[movie]["rating"] for movie in movies]
        average = get_average(ratings)
        median = get_median(ratings)
        best_movies = "; ".join([f"{movie}, {rating}" for movie, rating in get_best_movies(movies)])
        worst_movies = "; ".join([f"{movie}, {rating}" for movie, rating in get_worst_movies(movies)])
        print(f"Average rating: {average}")
        print(f"Median rating: {median}")
        print(f"Best movie: {best_movies}")
        print(f"Worst movie: {worst_movies}")

    def _command_random_movie(self):
        """Selects a random movie and displays it to the user"""
        movies = self._storage.list_movies()
        random_movie = random.choice(list(movies.keys()))
        print(f"Your movie tonight: {random_movie}, it's rated {movies[random_movie]['rating']}")


    def _command_search_movie(self):
        """Search if movie exits and supports auto-correct suggestions in case of typo made by the user"""
        movies = self._storage.list_movies()
        searched_movie = input("Enter part of movie: ")
        no_movie = True
        for movie in movies:
            if searched_movie.lower() in movie.lower():
                no_movie = False
                print(f"{movie}, {movies[movie]['rating']}")
        if no_movie:
            print(f"{searched_movie} doesn't exist!")
            suggestions = get_fuzz_suggestions(searched_movie, movies)
            if suggestions:
                print("Did you mean?")
            for suggestion in suggestions:
                print(suggestion[0])

    def _command_movies_sorted_by_rating(self):
        """Displays Movies sorted from most rated to less rated"""
        movies = self._storage.list_movies()
        ratings = list({movies[movie]["rating"] for movie in movies})
        ratings.sort(reverse=True)
        for rating in ratings:
            for movie in get_movies_based_on_rating(rating, movies):
                print(f"{movie[0]}: {movie[1]}")


    def _command_create_rating_histogram(self):
        """Creates a file containing histogram of the rating. File's name can be chosen by the user himself
           without the extension.
        """
        movies = self._storage.list_movies()
        ratings = [movies[movie]["rating"] for movie in movies]
        file_name = input("Enter the name of file you want to save to: ")
        plt.hist(ratings)
        plt.xlabel('Ratings', fontweight='bold', horizontalalignment='center')
        plt.ylabel('Number Of Films', fontweight='bold')
        plt.title("Distribution Of Ratings", fontweight='bold', color='blue', fontsize='14')
        plt.savefig(f"{file_name}.png")


    def _command_filter_movies(self):
        """Filters the movies based on minimum rating, start year, and end year and displays all
            movies in the chosen ranges. Entering empty string for a criteria will not set it.
        """
        minimum_rating = input_rating("Enter minimum rating (leave blank for no minimum rating): ", allow_blank=True)
        start_year = input_year("Enter start year (leave blank for no start year): ", allow_blank=True)
        end_year = input_year("Enter end year (leave blank for no end year): ", allow_blank=True)
        if not start_year:
            start_year = -3000
        if not end_year:
            end_year = 3000
        if end_year < start_year:
            end_year, start_year = start_year, end_year
        movies = self._storage.list_movies()
        filtered_movies = [(movie, movies[movie]["rating"], movies[movie]["year"]) for movie in movies
                           if (movies[movie]["rating"] >= minimum_rating and
                               start_year <= movies[movie]["year"] <= end_year)]
        for movie, rating, year in filtered_movies:
            print(f"{movie} ({rating}): {year}")

    def _exit(self):
        """Prints exit message before ending the program"""
        print("Bye!")

    def _generate_website(self):
        movies = self._storage.list_movies()
        html_elements = generate_html_elements(movies)
        with open("static/index_template.html", "r") as handler:
            original_html = handler.read()
        final_html = original_html.replace( "__TEMPLATE_MOVIE_GRID__", html_elements)

        with open("static/movies.html", "w") as handler:
            handler.write(final_html)
        print("\n Website generated successfully! \n")

    def run(self):
        print("********** My Movies Database **********")
        print("\t" * 3)
        while True:
            print(self._menu)
            user_input = input(f"Enter choice (0-{len(self._functions_mapping)-1}): ")
            print("\t" * 2)
            if not user_input.isnumeric() or int(user_input) not in range(len(self._functions_mapping)):
                print("Invalid Choice")
                continue
            self._functions_mapping[user_input]()
            if user_input == "0":
                break
            print("\t" * 2)
            input("Press enter to continue ")
            print("\t" * 2)
