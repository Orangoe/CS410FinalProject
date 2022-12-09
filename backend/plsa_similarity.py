import pandas
from pymongo import MongoClient
import re
from plsa.algorithms import PLSA
from plsa import Corpus, Pipeline
from plsa.pipeline import DEFAULT_PIPELINE
import numpy as np
import csv


def plsa_train(topic_num):
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['db_final']
    data = table_movies.find({}, {'_id': 0})
    movie_sim = []
    for d in data:
        movie_sim.append(d)
    client.close()

    movie_sim_pd = pandas.DataFrame(movie_sim)
    pattern = r"[0-9a-zA-Z\ -']+"
    stop_words = ["i", "me", "my", "myself",
                  "we", "our", "ours", "ourselves",
                  "you", "your", "yours",
                  "their", "they", "his", "her",
                  "she", "he", "a", "an", "and",
                  "is", "was", "are", "were",
                  "him", "himself", "has", "have",
                  "it", "its", "the", "us"]
    tokens = movie_sim_pd['movie_plot'].apply(lambda x: "".join(re.findall(pattern, x.lower())))
    new_tokens = []
    index = []
    for i, token in enumerate(tokens):
        words = token.split()
        stemmedlst = [word for word in words if not word in stop_words]
        new_tokens.append(' '.join(stemmedlst))
        index.append(i)
    movie_sim_pd['tokenized'] = new_tokens
    movie_sim_pd['index'] = index
    pipeline = Pipeline(*DEFAULT_PIPELINE)
    corpus = Corpus(new_tokens, pipeline)
    plsa = PLSA(corpus, topic_num, True)
    result = plsa.fit()
    plsa_result = result.topic_given_doc
    rows = []
    for doc in plsa_result.tolist():
        rows.append(doc)
    with open('train_model.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(rows)
    f.close()


def plsa_sim(movie_id):
    f = open("train_model.csv", 'r')
    new_result = []
    for line in f:
        row1 = []
        for num in line.strip().split(','):
            row1.append(float(num))
        new_result.append(row1)
    f.close()
    plsa_result = np.array(new_result)
    client = MongoClient('mongodb+srv://groupMember:1155665@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
    collection = 'MoviePlotDB'
    db = client[collection]
    table_movies = db['db_final']
    data = table_movies.find({}, {'_id': 0})
    movie_sim = []
    for d in data:
        movie_sim.append(d)
    client.close()

    movie_sim_pd = pandas.DataFrame(movie_sim)
    pattern = r"[0-9a-zA-Z\ -']+"
    stop_words = ["i", "me", "my", "myself",
                  "we", "our", "ours", "ourselves",
                  "you", "your", "yours",
                  "their", "they", "his", "her",
                  "she", "he", "a", "an", "and",
                  "is", "was", "are", "were",
                  "him", "himself", "has", "have",
                  "it", "its", "the", "us"]
    tokens = movie_sim_pd['movie_plot'].apply(lambda x: "".join(re.findall(pattern, x.lower())))
    new_tokens = []
    index = []
    for i, token in enumerate(tokens):
        words = token.split()
        stemmedlst = [word for word in words if not word in stop_words]
        new_tokens.append(' '.join(stemmedlst))
        index.append(i)
    movie_sim_pd['tokenized'] = new_tokens
    movie_sim_pd['index'] = index
    score_dict = {}
    target_movie = plsa_result[movie_sim_pd[movie_sim_pd['movie_id'] == movie_id]['index'].values[0]]
    for i, m in enumerate(plsa_result):
        value = np.sum(target_movie * m)
        if value > 0:
            mov = movie_sim_pd[movie_sim_pd['index'] == i]['movie_title'].values[0]
            score_dict[mov] = value
    top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    top_10 = []
    for tuple in top_10_tuple:
        top_10.append(tuple[0])
    return top_10


if __name__ == '__main__':
    plsa_train(10)
    print(plsa_sim("tt0499549"))
