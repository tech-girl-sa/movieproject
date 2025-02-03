from storage.istorage import IStorage
import csv


class StorageCsv(IStorage):

    def __init__(self, file_path):
        self.file_path = file_path


    def map_to_read(self, list_dicts):
        mapped_data = {
            movie["Title"]: {
                "rating": float(movie["Rating"]),
                "year": int(movie["Year"]),
                "poster": movie["Poster"],
                "notes" : movie["Notes"],
                "imdb_id": movie["ImdbID"],
                "country": movie["Country"]
            } for movie in list_dicts
        }
        return mapped_data


    def map_to_write(self, dict_dicts):
        mapped_data = [{"Title": movie, "Rating": dict_dicts[movie]["rating"],
                        "Year": dict_dicts[movie]["year"], "Poster": dict_dicts[movie]["poster"],
                        "Notes": dict_dicts[movie]["notes"], "ImdbID": dict_dicts[movie]["imdb_id"],
                        "Country": dict_dicts[movie]["notes"]
                        }
                       for movie in dict_dicts
                       ]
        return mapped_data


    def write_movies(self, movies):
        mapped_data = self.map_to_write(movies)
        with open(self.file_path, 'w', newline='') as csvfile:
            fieldnames = ['Title', 'Rating', 'Year', "Poster", "Notes", "ImdbID", "Country"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mapped_data)

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        For example, the function may return:
        {
          "Titanic": {
            "rating": 9,
            "year": 1999,
            "poster": link.png,
            "notes": ""
            "imdb_id": id
          },
          "..." {
            ...
          },
        }
        """
        try:
            with open(self.file_path, "r") as file:
                movies = list(csv.DictReader(file))
            mapped_data = self.map_to_read(movies)
        except FileNotFoundError:
            mapped_data = {}
            self.write_movies(mapped_data)
        return mapped_data


    def add_movie(self, title, year, rating, poster="", imdb_id="", country=""):
        movies = self.list_movies()
        movies[title] = {
            "rating": rating,
            "year": year,
            "poster": poster,
            "notes": "",
            "imdb_id": imdb_id,
            "country": country
        }
        self.write_movies(movies)


    def delete_movie(self, title):
        movies = self.list_movies()
        movies.pop(title)
        self.write_movies(movies)


    def update_movie(self, title, notes):
        movies = self.list_movies()
        movies[title]["notes"] = notes
        self.write_movies(movies)


