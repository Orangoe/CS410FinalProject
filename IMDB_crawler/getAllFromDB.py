import pymongo
from pymongo import MongoClient
import json


def main():
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['main']
    data = table_movies.find({}, {'_id': 0})
    data_list = []
    for d in data:
        data_list.append(d)
    with open("imdb_data.json", "w") as outfile:
        json.dump(data_list, outfile)

    client.close()


if __name__ == '__main__':
    main()
