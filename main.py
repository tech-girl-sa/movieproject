from movie_app import MovieApp
from storage_json import StorageJson


def main():
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()