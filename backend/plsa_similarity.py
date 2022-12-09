import pandas
from pymongo import MongoClient
import re
from plsa.algorithms import PLSA
from plsa import Corpus, Pipeline
from plsa.pipeline import DEFAULT_PIPELINE
import nltk
from nltk.corpus import stopwords
import numpy as np
import csv


def plsa_train(topic_num):
    nltk.download('stopwords', download_dir='E:/workspace/cs410/fp/backend/stopword_data')
    nltk.download('averaged_perceptron_tagger' , download_dir='E:/workspace/cs410/fp/backend/stopword_data')
    nltk.download('wordnet' , download_dir='E:/workspace/cs410/fp/backend/stopword_data')

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
    stop_words = set(stopwords.words('english'))
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
    plsa_result_raw = plsa.fit()
    plsa_result = plsa_result_raw.topic_given_doc
    rows = []
    for doc in plsa_result.tolist():
        rows.append(doc)
    with open('train_model.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(rows)
    f.close()
    print('completed PLSA training')


def plsa_sim(movie_id):
    f = open("train_model.csv", 'r')
    new_result = []
    for line in f:
        row1 = []
        for num in line.strip().split(','):
            if num == "":
                continue
            row1.append(float(num))

        new_result.append(row1)
    f.close()
    # print(type(new_result))
    # print(type(new_result[0]))
    # print(type(new_result[0][0]))
    plsa_result = np.array(new_result)
    nltk.download('stopwords', download_dir='E:/workspace/cs410/fp/backend/stopword_data')
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
    stop_words = set(stopwords.words('english'))
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
            mov = movie_sim_pd[movie_sim_pd['index'] == i]['movie_id'].values[0]
            score_dict[mov] = value
    top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[1:11]
    top_10 = []
    for t in top_10_tuple:
        top_10.append(t[0])
    return top_10


if __name__ == '__main__':
    result = plsa_train(5)
    plsa_sim("tt0499549", result)
