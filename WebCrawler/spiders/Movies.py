import scrapy
import LibraryScraper.items as items
from HelperFunctions import TextManipulation as TextManu
from urllib.parse import unquote
from HelperFunctions.GenerateUrlList import generate


class movieSpider(scrapy.Spider):
    """
    The spider for the scraper
    """
    name = 'Movies'
    allowed_domains = ['https://www.imdb.com/']

    def __init__(self, *args, **kwargs):
        super(MovieCrawler, self).__init__(*args, **kwargs)

        url = kwargs.get('start_url')
        self.start_urls = [url]
        self.max_plot = int(kwargs.get('num_plots'))
        self.completed_plot = False
        self.collection = kwargs.get('collection')

    def parse(self, response):
        """
        The parser for the spider, parsing all the data from a downloaded xml file.
        ALl attributes are positioned by their xpath
        """
        
        movie_url = response.request.url
        movie_id = unquote(movie_url)
        movie_id = TextManu.get_id(movie_id)

        item = items.movieScraperItem()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        overview = mainContent + '/div[2]/div[4]/div[1]/div[2]'

        title = response.xpath(overview + '/h1/text()').get()

        plot = response.xpath(overview + '/div[1]/span[2]/div/a/span/text()').extract()
        plot_url = response.xpath(overview + '/div[1]/span[2]/div/a/@href').extract()

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
        item['plot'] = plot
        item['plot_url'] = plot_url
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count

        # scrape the plot of the movie
        for link_plot in plot_url:
            yield scrapy.Request(link_plot, callback=self.parse_plot, dont_filter=False)

        # send data to pipeline
        yield item

        # check if the movie in the starting url does not have similar movies
        # to start the recursion
        if self.first_movie:
            self.first_movie = False
            if len(similar_movies) == 0:
                url_list = generate(self.start_urls[0], self.allowed_domains[0])
                for url in url_list:
                    yield scrapy.Request(url, callback=self.parse, dont_filter=False)

        # start the recursion and scrape all the movies in similar movie list
        for link_movie in similar_movies:
            yield scrapy.Request(link_movie, callback=self.parse, dont_filter=False)

    def parse_plot(self, response):
        """
        the parser for the spider to crawl the plots' website
        :param self defualt para for scrapy spiders
        :param response default para for scrapy spiders
        """
        if self.completed_plot:
            return
        plot_url = response.request.url

        plot_id = unquote(plot_url)
        plot_id = TextManu.get_id(plot_id)

        item = items.plotScraperItems()

        mainContent = '/html/body/div[2]/div[3]/div[1]'

        plotInfo = mainContent + '/div[2]/div[3]/div[2]'

        name = response.xpath(plotInfo + '/div[2]/h1//span/text()').get()
        plotXpath = [plotInfo + '/div[8]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[7]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[6]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[5]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[4]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[3]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[2]/div[1]/div[2]/div[1]/div[1]',
                            plotInfo + '/div[1]/div[1]/div[2]/div[1]/div[1]'
                            ]
        rating = response.xpath(plotXpath[0] + '/span[2]/span/text()').get()
        rating_count = response.xpath(plotXpath[0] + '/span[3]/span/text()').get()
        review_count = response.xpath(plotXpath[0] + '/span[4]/span/text()').get()

        for i in plotXpath[1:]:
            if rating is None:
                rating = response.xpath(i + '/span[2]/span/text()').get()
            if rating_count is None:
                rating_count = response.xpath(i + '/span[3]/span/text()').get()
            if review_count is None:
                review_count = response.xpath(i + '/span[4]/span/text()').get()

        rating = TextManu.get_rating(rating)
        rating_count = TextManu.get_num(rating_count)
        review_count = TextManu.get_num(review_count)

        related_plots_url = unquote(plot_url).replace('/show/', '/similar/')
        plot_movies_path = [plotInfo + '/div[8]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[7]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[6]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[5]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[4]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[3]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[2]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()',
                             plotInfo + '/div[1]/div[1]/div[2]/div[1]/table/tr[*]/td[2]/a/span/text()'
                             ]

        plot_movies = response.xpath(plot_movies_path[0]).extract()
        for i in plot_movies_path:
            if len(plot_movies) == 0:
                plot_movies = response.xpath(i).extract()

        item['name'] = name
        item['plot_url'] = plot_url
        item['plot_id'] = plot_id
        item['rating'] = rating
        item['rating_count'] = rating_count
        item['review_count'] = review_count

        yield item

        yield scrapy.Request(related_plots_url, callback=self.parse_related_plots, dont_filter=False)


