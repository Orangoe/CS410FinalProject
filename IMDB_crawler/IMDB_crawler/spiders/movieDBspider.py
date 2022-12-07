import scrapy
from ..items import ImdbCrawlerItem
from pymongo import MongoClient


class MoviedbspiderSpider(scrapy.Spider):
    name = 'movieDBspider'
    allowed_domains = ['']

    def __init__(self, *args, **kwargs):
        super(MoviedbspiderSpider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.client = MongoClient('mongodb+srv://peter:atlas894@cluster0.xmygnse.mongodb.net/?retryWrites=true&w=majority')
        self.collection = 'MoviePlotDB'
        self.db = self.client[self.collection]
        self.table_movies = self.db['db_final']
        data = self.table_movies.find({"movie_title": ""}, {'_id': 0})
        self.movie_urls_id_pairs = []
        for d in data:
            self.movie_urls_id_pairs.append((d['movie_id'], "https://www.imdb.com/title/" + d['movie_id'] + "/plotsummary?ref_=tt_stry_pl"))
        self.start_urls = []

    def start_requests(self):
        for (movie_id, url) in self.movie_urls_id_pairs:
            yield scrapy.Request(url, meta={'movie_id': movie_id})

    def parse(self, response):
        m_id = response.meta['movie_id']
        tv_s = response.xpath('//div[@div="quicklinks"]/span[1]/text()').get()
        title = response.xpath('//div[@class="subpage_title_block__right-column"]/div/h3/a/text()').get()
        if tv_s is not None:
            print(m_id, title, tv_s)
            # if tv_s == " (TV Series) ":
            return
        self.counter += 1
        item = ImdbCrawlerItem()
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
        item['movie_storyLines'] = storyLine_list
        item['movie_plot'] = storyLine_list[longest_index]
        item['movie_year'] = ""
        item['movie_level'] = ""
        item['movie_length'] = ""
        item['movie_genres'] = ""
        item['movie_score'] = ""
        yield item
