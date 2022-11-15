import scrapy
import LibraryScraper.items as items
from HelperFunctions import TextManipulation as TextManu
from urllib.parse import unquote
from HelperFunctions.GenerateUrlList import generate


class BookSpider(scrapy.Spider):
    """
    The spider for the scraper
    """
    name = 'Book'
    allowed_domains = ['www.goodreads.com']

    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)

        url = kwargs.get('start_url')
        self.start_urls = [url]
        self.max_book = int(kwargs.get('num_books'))
        self.completed_book = False
        self.max_author = int(kwargs.get('num_authors'))
        self.completed_author = False
        self.collection = kwargs.get('collection')
        self.first_book = True

    def parse(self, response):
        """
        The parser for the spider, parsing all the data from a downloaded xml file.
        ALl attributes are positioned by their xpath
        """
        if self.completed_book:
            return

        book_url = response.request.url
        book_id = unquote(book_url)
        book_id = TextManu.get_id(book_id)

        item = items.BookScraperItem()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        bookInfo = mainContent + '/div[2]/div[4]/div[1]/div[2]'

        title = response.xpath(bookInfo + '/h1/text()').get()

        ISBN = response.xpath(bookInfo + '/div[5]/div[3]/div[1]/div[2]/div[2]/text()').get()
        ISBN = TextManu.testISBN(ISBN)
        if len(ISBN) == 0:
            ISBN = response.xpath(bookInfo + '/div[5]/div[3]/div[1]/div[1]/div[2]/text()').get()
            ISBN = TextManu.testISBN(ISBN)

        author = response.xpath(bookInfo + '/div[1]/span[2]/div/a/span/text()').extract()
        author_url = response.xpath(bookInfo + '/div[1]/span[2]/div/a/@href').extract()

        rating = response.xpath(bookInfo + '/div[2]/span[2]/text()').get()
        rating = TextManu.get_rating(rating)

        rating_count = response.xpath(bookInfo + '/div[2]/a[2]/text()')[1].get()
        rating_count = TextManu.get_num(rating_count)

        review_count = response.xpath(bookInfo + '/div[2]/a[3]/text()')[1].get()
        review_count = TextManu.get_num(review_count)

        image_url_raw = mainContent + '/div[2]//div[4]/div[1]/div[1]/div[1]/div[1]/a/@href'
        image_url = urlImg if len(urlImg := response.xpath(image_url_raw).extract()) > 0 else None
        if image_url is not None:
            image_url = 'https://www.goodreads.com' + unquote(image_url[0])
        else:
            image_url = ''

        similar_books = response.xpath(mainContent +
                                       '/div[2]/div[5]/div[3]/div/div[2]/div/div[1]/div[1]/ul/li[*]/a/@href').extract()

        # get rid of the spaces and /n in the text extracted.
        title = TextManu.text_extract(title)

        item['book_url'] = book_url
        item['title'] = title
        item['book_id'] = book_id
        item['ISBN'] = ISBN
        item['author'] = author
        item['author_url'] = author_url
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count
        item['image_url'] = image_url
        item['similar_books'] = similar_books

        # scrape the author of the book
        for link_author in author_url:
            yield scrapy.Request(link_author, callback=self.parse_author, dont_filter=False)

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

    def parse_author(self, response):
        """
        the parser for the spider to crawl the authors' website
        :param self defualt para for scrapy spiders
        :param response default para for scrapy spiders
        """
        if self.completed_author:
            return
        author_url = response.request.url

        author_id = unquote(author_url)
        author_id = TextManu.get_id(author_id)

        item = items.AuthorScraperItems()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        authorInfo = mainContent + '/div[2]/div[3]/div[2]'

        pic = mainContent + '/div[2]/div[3]/div[1]/a[1]/img/@src'

        name = response.xpath(authorInfo + '/div[2]/h1//span/text()').get()
        book_stats_xpath = [authorInfo + '/div[8]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[7]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[6]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[5]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[4]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[3]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[2]/div[1]/div[2]/div[1]/div[1]',
                            authorInfo + '/div[1]/div[1]/div[2]/div[1]/div[1]'
                            ]
        rating = response.xpath(book_stats_xpath[0] + '/span[2]/span/text()').get()
        rating_count = response.xpath(book_stats_xpath[0] + '/span[3]/span/text()').get()
        review_count = response.xpath(book_stats_xpath[0] + '/span[4]/span/text()').get()

        for i in book_stats_xpath[1:]:
            if rating is None:
                rating = response.xpath(i + '/span[2]/span/text()').get()
            if rating_count is None:
                rating_count = response.xpath(i + '/span[3]/span/text()').get()
            if review_count is None:
                review_count = response.xpath(i + '/span[4]/span/text()').get()

        rating = TextManu.get_rating(rating)
        rating_count = TextManu.get_num(rating_count)
        review_count = TextManu.get_num(review_count)

        image_url_raw = response.xpath(pic).extract()
        image_url = ''

        related_authors_url = unquote(author_url).replace('/show/', '/similar/')

        if len(image_url_raw) != 0:
            image_url = unquote(image_url_raw[0])
        author_books_path = [authorInfo + '/div[8]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[7]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[6]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[5]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[4]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[3]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[2]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             authorInfo + '/div[1]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()'
                             ]

        author_books = response.xpath(author_books_path[0]).extract()
        for i in author_books_path:
            if len(author_books) == 0:
                author_books = response.xpath(i).extract()

        item['name'] = name
        item['author_url'] = author_url
        item['author_id'] = author_id
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count
        item['image_url'] = image_url
        item['related_authors'] = []
        item['author_books'] = author_books

        yield item

        yield scrapy.Request(related_authors_url, callback=self.parse_related_authors, dont_filter=False)

    def parse_related_authors(self, response):
        """
        the parser for the spider to crawl the website for related authors.
        :param self defualt para for scrapy spiders
        :param response default para for scrapy spiders
        """

        author_url = response.request.url
        author_id = unquote(author_url)
        author_id = TextManu.get_id(author_id)
        related_authors = response.xpath('/html/body/div[4]/div[1]/'
                                         'div[3]/div[1]/div[5]/div/div[*]/div/div/div[2]/div[1]/a/@href').extract()

        if related_authors is None:
            related_authors = response.xpath('/html/body/div[4]/div[1]'
                                             '/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]'
                                             '/div[1]/div[2]/div[1]/a/@href').extract()
            if related_authors is None:
                related_authors = response.xpath('/html/body/div[4]/div[1]'
                                                 '/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]'
                                                 '/div/div[2]/div[1]/a/@href').extract()
            else:
                related_authors.append(response.xpath('/html/body/div[4]/div[1]'
                                                      '/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]'
                                                      '/div/div[2]/div[1]/a/@href').extract()[0])
        else:
            related_authors.append(response.xpath('/html/body/div[4]/div[1]'
                                                  '/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]'
                                                  '/div/div[2]/div[1]/a/@href').extract()[0])
            related_authors.append(response.xpath('/html/body/div[4]/div[1]'
                                                  '/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]'
                                                  '/div/div[2]/div[1]/a/@href').extract()[0])

        item = items.RelatedAuthorsItems()
        item['author_id'] = author_id
        item['related_authors'] = related_authors

        yield item

        # for link_author in related_authors:
        #     yield scrapy.Request(link_author, callback=self.parse_author, dont_filter=False)
