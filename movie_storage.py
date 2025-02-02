import json


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open("movies.json","r") as file:
        data = json.loads(file.read())
    return data


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = list_movies()
    movies[title] = {
        "rating": rating,
        "year": year
    }
    with open("movies.json", "w") as file:
        file.write(json.dumps(movies))


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = list_movies()
    movies.pop(title)
    with open("movies.json", "w") as file:
        file.write(json.dumps(movies))


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = list_movies()
    movies[title]["rating"] = rating
    with open("movies.json", "w") as file:
        file.write(json.dumps(movies))
  