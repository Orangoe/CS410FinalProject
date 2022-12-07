from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from IMDB.items import Movie


class IMDBSpider(CrawlSpider):
    name = 'imdbtops'
    # allowed_domains = ['imbd.com']
    start_urls = ['http://www.imdb.com/chart/top', ]

    linkExtractor = LxmlLinkExtractor(allow=(r'/title/tt\d+/[\w?=]+'), tags=('a', 'title'), attrs=('href',),
                                      unique=True)

    rules = [Rule(linkExtractor, callback="parse_items", follow=False)]

    def get_text(self, tag):
        if tag:
            return tag.text.strip()
        else:
            return ''

    def parse_items(self, response):
        soup = BeautifulSoup(response.body)
        movie = Movie()
        movie['movieName'] = soup.h1.span.text
        movie['movieRating'] = self.get_text(soup.find('div', attrs={'class': 'titlePageSprite'}))
        movie['moviePlot'] = self.get_text(soup.find('p', attrs={'itemprop': 'description'}))
        movie['movieReleaseDate'] = self.get_text(soup.find('a', attrs={'title': 'See all release dates'}))
        movie['movieGenres'] = [gnr.text for gnr in soup.find_all('span', attrs={'itemprop': 'genre'})]

        return movie
