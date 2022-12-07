# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = scrapy.Field()
    movie_title = scrapy.Field()
    movie_poster = scrapy.Field()
    movie_year = scrapy.Field()
    movie_length = scrapy.Field()
    movie_level = scrapy.Field()
    movie_genres = scrapy.Field()
    movie_score = scrapy.Field()
    movie_storyLines = scrapy.Field()
    movie_plot = scrapy.Field()
    pass
