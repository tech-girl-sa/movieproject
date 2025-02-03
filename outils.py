import flag
import pycountry
from pycountry.db import Country
from thefuzz import process

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


def input_year(prompt_message="Enter the movie's year: ", allow_blank = False):
    while True:
        year = input(prompt_message)
        if allow_blank and not year:
            return year
        try:
            year = int(year)
            return year
        except ValueError:
            print(f"Year {year} is not valid.")

def input_data_manual_entry():
    while True:
        user_input = input("We couldn't fetch year and rating of the movie automatically."
                           "if you are sre you entered the right movie name and want to continue "
                           "entering those values manually press Y else press N to cancel adding the movie.")
        if user_input.lower() in ["y", "n"]:
            return user_input.lower()
        else:
            print("Invalid Input")


def get_fuzz_suggestions(movie,movies):
    list_movies = list(movies.keys())
    suggestions=process.extract(movie,list_movies)
    accurate_suggestions = [suggestion for suggestion in suggestions if suggestion[1] >= 73]
    return accurate_suggestions


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


def get_country_flag_emoji(country:Country):
    if country:
        flags=""
        try:
            countries = country.split(",")
            for country in countries:
                country_obj = pycountry.countries.search_fuzzy(country)[0]
                country_code = country_obj.alpha_2
                flags += flag.flag(country_code)
            return flags
        except Exception:
            return ""
    else:
        return ""


def map_html_element(movie_title, movie_info):
    year = movie_info["year"]
    notes = movie_info["notes"]
    rating = movie_info["rating"]
    imdb_id = movie_info["imdb_id"]
    country = movie_info["country"]
    if movie_info["poster"] and len(movie_info["poster"]) > 3:
        poster = movie_info["poster"]
    else:
        poster = "https://placehold.co/400x600?text=Missing+Photo&font=roboto"
    if imdb_id:
        imdb_link=f"https://www.imdb.com/title/{imdb_id}/"
    else:
        imdb_link = "https://www.imdb.com"
    country_flag = get_country_flag_emoji(country)
    return f"""<li> 
                <div class="movie">
                <a href="{imdb_link}">
                <img class="movie-poster" title="{notes}" src="{poster}">
                </a>
                <div class="title-area">
                <div class="movie-title">{movie_title}</div>
                <span class="badge">{rating}</span>
                </div>
                <div class="movie-year"><span class="flags">{country_flag}</span> {year}</div>
                </div> 
               </li>"""


def generate_html_elements(movies):
    html_elements = ""
    for movie in movies:
        html_elements += map_html_element(movie, movies[movie])
    return html_elements