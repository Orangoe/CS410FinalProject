from pymongo import MongoClient
from bson.json_util import dumps, loads
import re


def get_by_id(movie_id):
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['db_final']
    data = table_movies.find({'movie_id': str(movie_id)}, {'_id': 0})
    data = list(data)
    return data


def get_by_multiple_id_brief(movie_id_list):
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['db_final']
    data = []
    for movie_id in movie_id_list:
        data += list(table_movies.find({'movie_id': str(movie_id)}, {'_id': 0, 'movie_id': 1, 'movie_title': 1, 'movie_poster': 1,
                                                                     'movie_year': 1, 'movie_level': 1, 'movie_genres': 1,
                                                                     'movie_score': 1}))
    data = list(data)
    return data


def get_by_title(movie_title):
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['db_final']
    movie_title_re = re.compile(str(movie_title), re.IGNORECASE)
    data = table_movies.find({'movie_title': movie_title_re}, {'_id': 0, 'movie_id': 1, 'movie_title': 1, 'movie_poster': 1,
                                                                     'movie_year': 1, 'movie_level': 1, 'movie_genres': 1,
                                                                     'movie_score': 1})
    data = list(data)
    return data
