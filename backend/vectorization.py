import pandas
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def vectorization(movie_input, type):
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
    for token in tokens:
        words = token.split()
        stemmedlst = [word for word in words if not word in stop_words]
        new_tokens.append(' '.join(stemmedlst))
    movie_sim_pd['tokenized'] = new_tokens
    if type == "plot":
        selected_movie = "".join(re.findall(pattern, movie_input.lower()))
    else:
        selected_movie = movie_sim_pd.loc[movie_sim_pd['movie_id'] == str(movie_input)].tokenized.values[0]
    score_dict = {}
    for i in movie_sim_pd['movie_id']:
        movie = movie_sim_pd.loc[movie_sim_pd['movie_id'] == str(i)].tokenized.values[0]
        target_vector = [selected_movie, movie]
        vectorizer = CountVectorizer(stop_words='english')
        vectorizer.fit_transform(target_vector)
        a, b = vectorizer.transform([target_vector[0]]), vectorizer.transform([target_vector[1]])
        score = cosine_similarity(a, b)
        score_dict[i] = score[0][0]
    if type == "plot":
        top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    else:
        top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[1:11]
    top_10 = []
    for tuple in top_10_tuple:
        top_10.append(tuple[0])
    return top_10

if __name__ == '__main__':
    print(vectorization("tt0499549","id"))
    print(vectorization("In the near future, when the inflating Sun is threatening all lives on Earth, governments are united together to carry out an ambitious plan: building thousands of gigantic thrusters on the ground to push our planet out of the solar system. They call it Project Wandering Earth. 17 years later, the plan is in danger of catastrophic failure when the Earth is traveling near Jupiter. With only 37 hours to spare, teams of rescuers rush to save the Earth from colliding with Jupiter. A young man, Liu Qi, his sister and his grandpa are involuntarily involved in this biggest rescue mission of the history. Together, they will encounter many difficulties along the road, they will revisit their past, and they will feel desperation and hope. This is a story about uniting all humans to face enormous challenges, about strong feelings between father and son, and most importantly, about hope in despair.", "plot"))