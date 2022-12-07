import pandas
from pymongo import MongoClient
from rank_bm25 import *
import re


def BM25_IMBD(movie_id):
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
    stop_words = ["i", "me", "my", "myself",
                  "we", "our", "ours", "ourselves",
                  "you", "your", "yours",
                  "their", "they", "his", "her",
                  "she", "he", "a", "an", "and",
                  "is", "was", "are", "were",
                  "him", "himself", "has", "have",
                  "it", "its", "the", "us"]
    # stop_words = []

    pattern = r"[0-9a-zA-Z\ -']+"
    movie_sim_pd['tokenized'] = movie_sim_pd['movie_plot'].apply(lambda x:  "".join(re.findall(pattern, x.lower())))
    # selected_movie = movie_sim_pd.loc[movie_sim_pd['movie_title'] == ""]
    selected_movie = movie_sim_pd.loc[movie_sim_pd['movie_id'] == str(movie_id)]
    selected_token_list = selected_movie.tokenized.values[0].split(' ')
    model_tokens_list = movie_sim_pd.tokenized.values.tolist()
    for i, token in enumerate(model_tokens_list):
        model_tokens_list[i] = token.split(' ')

    print(selected_movie['movie_plot'])
    # print(selected_token_list)
    bm25 = BM25Okapi(model_tokens_list)
    movie_sim_pd['Similarity Score'] = bm25.get_scores(selected_token_list)
    top_10 = bm25.get_top_n(selected_token_list, movie_sim_pd['movie_storyLines'], n=10)
    df_final = movie_sim_pd[movie_sim_pd['movie_storyLines'].isin(top_10)]
    df_final = df_final.sort_values(by='Similarity Score', ascending=False)
    print(df_final['movie_title'])
    print(df_final.movie_id.values.tolist())
    return df_final.movie_id.values.tolist()


if __name__ == '__main__':
    BM25_IMBD("tt0499549")
