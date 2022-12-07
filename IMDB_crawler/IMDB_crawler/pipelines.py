# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from pymongo import MongoClient


class ImdbCrawlerPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.client = MongoClient('mongodb+srv://peter:atlas894@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
        self.collection = 'MoviePlotDB'
        self.db = self.client[self.collection]
        self.table_movies = self.db['db_final']
        self.new_data = 0
        self.crawler = crawler

    def process_item(self, item, spider):
        # if spider.name == "movieDBspider":
        #     if self.table_movies.count_documents({'$and': [
        #         {'movie_title': {'$not': item["movie_title"]}},
        #         {'movie_id': item["movie_id"]}
        #     ]}, limit=1) == 0:
        #         self.table_movies.update_one({'movie_id': item["movie_id"]},
        #                                  {'$set': {"movie_title": item["movie_title"],
        #                                            "movie_poster": item["movie_poster"],
        #                                            "movie_storyLines": item["movie_storyLines"],
        #                                            "movie_plot": item["movie_plot"]}},
        #                                  upsert=False)

        if self.table_movies.count_documents({'movie_id': item["movie_id"]}, limit=1) == 0:
            self.table_movies.insert_one(dict(item))
            self.new_data += 1
        else:
            if item['movie_plot'] is not "":
                self.table_movies.update_one({'movie_id': item["movie_id"]},
                                         {'$set': {"movie_title": item["movie_title"],
                                                   "movie_poster": item["movie_poster"],
                                                   "movie_storyLines": item["movie_storyLines"],
                                                   "movie_plot": item["movie_plot"]}},
                                         upsert=False)
            elif item['movie_year'] is not "":
                self.table_movies.update_one({'movie_id': item["movie_id"]},
                                         {'$set': {"movie_year": item["movie_year"],
                                                   "movie_length": item["movie_length"],
                                                   "movie_level": item["movie_level"],
                                                   "movie_genres": item["movie_genres"],
                                                   "movie_score": item["movie_score"]}},
                                         upsert=False)
        if self.new_data >= 500:
            self.crawler.engine.close_spider(spider, "got 500 new movies")
        return item
