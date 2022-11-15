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
        self.table_books = self.db['books']
        self.table_authors = self.db['authors']
        self.check_book = []
        self.check_author = []
        self.check_related_author = []
        self.crawler = crawler

    def process_item(self, item, spider):
        if self.collection != spider.collection:
            self.collection = spider.collection

        if len(self.check_book) >= spider.max_book\
                and spider.max_author <= len(self.check_author) == len(self.check_related_author):
            self.crawler.engine.close_spider(spider, "book and author full")
            return item

        if item.get('book_id', False):
            if len(self.check_book) < spider.max_book:
                book_id = item['book_id']
                if book_id in self.check_book:
                    raise DropItem(item)
                self.check_book.append(book_id)

                self.table_books.insert_one(dict(item))
                print("stored book " + book_id)
                # spider.count_book += 1
            else:
                spider.completed_book = True
        elif item.get('author_url', False):
            if len(self.check_author) < spider.max_author:
                author_id = item['author_id']
                if author_id in self.check_author:
                    raise DropItem(item)
                self.check_author.append(author_id)

                self.table_authors.insert_one(dict(item))
                print("stored author " + author_id)
                # spider.count_author += 1
            else:
                spider.completed_author = True

        else:
            author_id = item['author_id']
            if author_id in self.check_related_author:
                raise DropItem(item)
            if author_id in self.check_author:
                self.check_related_author.append(author_id)
                query = {"author_id": author_id}
                update = {"$set": {"related_authors": item['related_authors']}}
                self.table_authors.find_one_and_update(query, update)

        return item
