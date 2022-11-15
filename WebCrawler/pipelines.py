# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import LibraryScraper.settings as settings


class LibarayscraperPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.client = MongoClient('localhost', 27017)
        self.collection = 'library'
        self.db = self.client[self.collection]
        self.table_movies = self.db['movies']
        self.table_plot = self.db['plot']
        self.check_movie = []
        self.check_plot = []
        self.crawler = crawler

    def process_item(self, item, spider):
        if self.collection != spider.collection:
            self.collection = spider.collection

        if len(self.check_movie) >= spider.max_movie\
                and spider.max_plot <= len(self.check_plot) == len(self.check_related_plot):
            self.crawler.engine.close_spider(spider, "movie and plot full")
            return item

        if item.get('movie_id', False):
            if len(self.check_movie) < spider.max_movie:
                movie_id = item['movie_id']
                if movie_id in self.check_movie:
                    raise DropItem(item)
                self.check_movie.append(movie_id)

                self.table_movies.insert_one(dict(item))
                print("stored movie " + movie_id)
                # spider.count_movie += 1
            else:
                spider.completed_movie = True
        elif item.get('plot_url', False):
            if len(self.check_plot) < spider.max_plot:
                plot_id = item['plot_id']
                if plot_id in self.check_plot:
                    raise DropItem(item)
                self.check_plot.append(plot_id)

                self.table_plot.insert_one(dict(item))
                print("stored plot " + plot_id)
                # spider.count_plot += 1
            else:
                spider.completed_plot = True

        else:
            plot_id = item['plot_id']
            if plot_id in self.check_related_plot:
                raise DropItem(item)
            if plot_id in self.check_plot:
                self.check_related_plot.append(plot_id)
                query = {"plot_id": plot_id}
                update = {"$set": {"related_plot": item['related_plot']}}
                self.table_plot.find_one_and_update(query, update)

        return item
