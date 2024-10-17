from functools import lru_cache
import json
import os


@lru_cache(maxsize=None)
def load_data(filename):
    """
    Loads data from the provided JSON file only once.
    Subsequent calls return the cached data.
    """
    file_path = os.path.join('data', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
