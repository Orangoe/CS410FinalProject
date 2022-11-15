# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    book_url = scrapy.Field()

    title = scrapy.Field()

    book_id = scrapy.Field()

    ISBN = scrapy.Field()

    author_url = scrapy.Field()

    author = scrapy.Field()

    rating = scrapy.Field()

    rating_count = scrapy.Field()

    review_count = scrapy.Field()

    image_url = scrapy.Field()

    similar_books = scrapy.Field()

    pass


class AuthorScraperItems(scrapy.Item):
    name = scrapy.Field()

    author_url = scrapy.Field()

    author_id = scrapy.Field()

    rating = scrapy.Field()

    rating_count = scrapy.Field()

    review_count = scrapy.Field()

    image_url = scrapy.Field()

    related_authors = scrapy.Field()

    author_books = scrapy.Field()

    pass


class RelatedAuthorsItems(scrapy.Item):
    author_id = scrapy.Field()

    related_authors = scrapy.Field()

    pass
