import scrapy
from ..items import ImdbCrawlerItem


class MoviespiderSpider(scrapy.Spider):
    name = 'movieSpider'
    allowed_domains = ['www.imdb.com']
    search_kw_list = []
    # start_urls = ['https://www.imdb.com/find/?q=a&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=b&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=c&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=d&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=e&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=star&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=the&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=f&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=g&s=tt&ttype=ft&ref_=fn_ft',
    #               'https://www.imdb.com/find/?q=h&s=tt&ttype=ft&ref_=fn_ft'
    #               ]
    start_urls = ['https://www.imdb.com/find/?q=star&s=tt&ttype=ft&ref_=fn_ft']


    def __init__(self, *args, **kwargs):
        super(MoviespiderSpider, self).__init__(*args, **kwargs)
        self.counter = 0

    def parse(self, response):
        url_list = response.xpath('//a[@class="ipc-metadata-list-summary-item__t"]/@href').getall()
        for raw_url in url_list:
            movie_id = raw_url.split('/')[2]
            detail_url = "https://www.imdb.com" + raw_url
            plot_url = "https://www.imdb.com/title/" + movie_id + "/plotsummary?ref_=tt_stry_pl"
            yield scrapy.Request(detail_url, callback=self.parse_detail_page)
            request_plot = scrapy.Request(plot_url, callback=self.parse_plot_page)
            request_plot.cb_kwargs['m_id'] = movie_id
            yield request_plot



    def parse_detail_page(self, response):
        # get recommended movies
        title = response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').get()
        # plot = response.xpath('//div[@data-testid="plot"]/span[@data-testid="plot-l"]/text()').get()
        related_movie_url_list = response.xpath('//div[@data-testid="shoveler-items-container"]/div/div/a/@href').getall()
        for raw_url in related_movie_url_list:
            movie_id = raw_url.split('/')[2]
            detail_url = "https://www.imdb.com" + raw_url
            plot_url = "https://www.imdb.com/title/" + movie_id + "/plotsummary?ref_=tt_stry_pl"
            yield scrapy.Request(detail_url, callback=self.parse_detail_page)
            request_plot = scrapy.Request(plot_url, callback=self.parse_plot_page)
            request_plot.cb_kwargs['m_id'] = movie_id
            yield request_plot

    def parse_plot_page(self, response, m_id):
        self.counter += 1
        item = ImdbCrawlerItem()
        title = response.xpath('//div[@class="subpage_title_block__right-column"]/div/h3/a/text()').get()
        year = response.xpath('//div/ul[@data-testid="hero-title-block__metadata"]/li[0]/a/text()').get()
        level = response.xpath('//div/ul[@data-testid="hero-title-block__metadata"]/li[1]/a/text()').get()
        length = response.xpath('//div/ul[@data-testid="hero-title-block__metadata"]/li[2]/a/text()').get()
        genres = response.xpath('//div[@data-testid="genres"]/div[1]/a/span/text()').getall()
        score = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[0]/text()').get()

        storyLine_list = response.xpath('//ul[@id="plot-summaries-content"]/li/p/text()').getall()

        longest = 0
        longest_index = 0
        for i, plot in enumerate(storyLine_list):
            if len(plot) > longest:
                longest = len(plot)
                longest_index = i

        image_url_raw = response.xpath('//div[@class="subpage_title_block"]/a/img/@src').get()
        image_url = ""
        if image_url_raw is not None:
            image_url_list = image_url_raw.split('.')[:-2]
            image_type = image_url_raw.split('.')[-1]
            for partial_url in image_url_list:
                image_url += partial_url + "."
            image_url += image_type
        print(str(self.counter) + " " + title)
        item['movie_id'] = m_id
        item['movie_title'] = title
        item['movie_poster'] = image_url
        item['movie_year'] = year
        item['movie_level'] = level
        item['movie_length'] = length
        item['movie_genres'] = genres
        item['movie_score'] = score
        item['movie_storyLines'] = storyLine_list
        item['movie_plot'] = storyLine_list[longest_index]
        yield item

