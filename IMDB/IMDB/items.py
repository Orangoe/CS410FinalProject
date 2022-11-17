# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movieID = scrapy.Field()
    movieName = scrapy.Field()
    moviePlot = scrapy.Field()
    movieGenres = scrapy.Field()
    movieRating = scrapy.Field()
    movieReleaseDate = scrapy.Field()


    pass
