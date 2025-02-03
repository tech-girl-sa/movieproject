from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson
import sys


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "movies.json"
    file_path = f"data/{file_name}"
    if file_name[-5:] == ".json":
        storage = StorageJson(file_path)
    elif file_name[-4:] == ".csv":
        storage = StorageCsv(file_path)
    else:
        #default to json storage
        file_path += ".json"
        storage = StorageJson(file_path)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()