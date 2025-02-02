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