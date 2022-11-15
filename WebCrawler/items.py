# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class movieScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    movie_url = scrapy.Field()

    title = scrapy.Field()

    movie_id = scrapy.Field()

    plot_url = scrapy.Field()

    plot = scrapy.Field()

    rating = scrapy.Field()

    review_count = scrapy.Field()

    critic_review_count = scrapy.Field()

    genre = scrapy.Field()

    cast = scrapy.Field()

    overview = scrapy.Field()

    writers = scrapy.Field()

    boxOffice = scrapy.Field()


    pass


class plotScraperItems(scrapy.Item):
    name = scrapy.Field()

    plot_url = scrapy.Field()

    plot_id = scrapy.Field()

    rating = scrapy.Field()

    rating_count = scrapy.Field()

    review_count = scrapy.Field()

    pass