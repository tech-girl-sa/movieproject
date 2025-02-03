import json

from storage.istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
            Returns a dictionary of dictionaries that
            contains the movies information in the database.

            The function loads the information from the JSON
            file and returns the data.

            For example, the function may return:
            {
              "Titanic": {
                "rating": 9,
                "year": 1999,
                "poster": link.png
              },
              "..." {
                ...
              },
            }
            """
        with open(self.file_path, "r") as file:
            data = json.loads(file.read())
        return data

    def add_movie(self, title, year, rating, poster=""):
        """
            Adds a movie to the movies database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        movies[title] = {
            "rating": rating,
            "year": year,
            "poster": poster
        }
        with open(self.file_path, "w") as file:
            file.write(json.dumps(movies))

    def delete_movie(self, title):
        """
            Deletes a movie from the movies database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
        """

        movies = self.list_movies()
        movies.pop(title)
        with open(self.file_path, "w") as file:
            file.write(json.dumps(movies))

    def update_movie(self, title, rating):
        """
            Updates a movie from the movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        movies[title]["rating"] = rating
        with open(self.file_path, "w") as file:
            file.write(json.dumps(movies))


