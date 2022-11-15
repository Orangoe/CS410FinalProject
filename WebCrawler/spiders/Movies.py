import scrapy
import LibraryScraper.items as items
from HelperFunctions import TextManipulation as TextManu
from urllib.parse import unquote
from HelperFunctions.GenerateUrlList import generate


class BookSpider(scrapy.Spider):
    """
    The spider for the scraper
    """
    name = 'Movies'
    allowed_domains = ['https://www.imdb.com/']

    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('start_url')
        self.start_urls = [url]
        self.max_producer = int(kwargs.get('num_producers'))
        self.completed_producer = False
        self.collection = kwargs.get('collection')

    def parse(self, response):
        """
        The parser for the spider, parsing all the data from a downloaded xml file.
        ALl attributes are positioned by their xpath
        """
        
        movie_url = response.request.url
        movie_id = unquote(movie_url)
        movie_id = TextManu.get_id(movie_id)

        item = items.BookScraperItem()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        overview = mainContent + '/div[2]/div[4]/div[1]/div[2]'

        title = response.xpath(overview + '/h1/text()').get()

        producer = response.xpath(overview + '/div[1]/span[2]/div/a/span/text()').extract()
        producer_url = response.xpath(overview + '/div[1]/span[2]/div/a/@href').extract()

        rating = response.xpath(overview + '/div[2]/span[2]/text()').get()
        rating = TextManu.get_rating(rating)

        rating_count = response.xpath(overview + '/div[2]/a[2]/text()')[1].get()
        rating_count = TextManu.get_num(rating_count)

        review_count = response.xpath(overview + '/div[2]/a[3]/text()')[1].get()
        review_count = TextManu.get_num(review_count)


        # get rid of the spaces and /n in the text extracted.
        title = TextManu.text_extract(title)

        item['movie_url'] = movie_url
        item['title'] = title
        item['movie_id'] = movie_id
        item['producer'] = producer
        item['producer_url'] = producer_url
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count

        # scrape the producer of the book
        for link_producer in producer_url:
            yield scrapy.Request(link_producer, callback=self.parse_producer, dont_filter=False)

        # send data to pipeline
        yield item

        # check if the book in the starting url does not have similar books
        # to start the recursion
        if self.first_book:
            self.first_book = False
            if len(similar_books) == 0:
                url_list = generate(self.start_urls[0], self.allowed_domains[0])
                for url in url_list:
                    yield scrapy.Request(url, callback=self.parse, dont_filter=False)

        # start the recursion and scrape all the books in similar book list
        for link_book in similar_books:
            yield scrapy.Request(link_book, callback=self.parse, dont_filter=False)

    def parse_producer(self, response):
        """
        the parser for the spider to crawl the producers' website
        :param self defualt para for scrapy spiders
        :param response default para for scrapy spiders
        """
        if self.completed_producer:
            return
        producer_url = response.request.url

        producer_id = unquote(producer_url)
        producer_id = TextManu.get_id(producer_id)

        item = items.producerScraperItems()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        producerInfo = mainContent + '/div[2]/div[3]/div[2]'

        name = response.xpath(producerInfo + '/div[2]/h1//span/text()').get()
        producerXpath = [producerInfo + '/div[8]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[7]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[6]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[5]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[4]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[3]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[2]/div[1]/div[2]/div[1]/div[1]',
                            producerInfo + '/div[1]/div[1]/div[2]/div[1]/div[1]'
                            ]
        rating = response.xpath(producerXpath[0] + '/span[2]/span/text()').get()
        rating_count = response.xpath(producerXpath[0] + '/span[3]/span/text()').get()
        review_count = response.xpath(producerXpath[0] + '/span[4]/span/text()').get()

        for i in producerXpath[1:]:
            if rating is None:
                rating = response.xpath(i + '/span[2]/span/text()').get()
            if rating_count is None:
                rating_count = response.xpath(i + '/span[3]/span/text()').get()
            if review_count is None:
                review_count = response.xpath(i + '/span[4]/span/text()').get()

        rating = TextManu.get_rating(rating)
        rating_count = TextManu.get_num(rating_count)
        review_count = TextManu.get_num(review_count)

        related_producers_url = unquote(producer_url).replace('/show/', '/similar/')
        producer_books_path = [producerInfo + '/div[8]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[7]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[6]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[5]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[4]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[3]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[2]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             producerInfo + '/div[1]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()'
                             ]

        producer_books = response.xpath(producer_books_path[0]).extract()
        for i in producer_books_path:
            if len(producer_books) == 0:
                producer_books = response.xpath(i).extract()

        item['name'] = name
        item['producer_url'] = producer_url
        item['producer_id'] = producer_id
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count

        yield item

        yield scrapy.Request(related_producers_url, callback=self.parse_related_producers, dont_filter=False)


