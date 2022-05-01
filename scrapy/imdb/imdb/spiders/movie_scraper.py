import scrapy

class Movie(scrapy.Item):
    title = scrapy.Field()
    IMDb_rating = scrapy.Field()
    popularity = scrapy.Field()
    genre = scrapy.Field()


class LinksSpider(scrapy.Spider):
    name = 'movie_scraper'
    allowed_domains = ['https://www.imdb.com/']
    try:
        with open("link_list.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response, **kwargs):
        p = Movie()

        title_xpath = '//h1/text()'
        score_xpath = '//div[@data-testid = "hero-rating-bar__aggregate-rating__score"]/span/text()'
        popularity_xpath = '//div[@data-testid = "hero-rating-bar__popularity__score"]/text()'
        genres_xpath = '//div[@data-testid = "genres"]/a/span/text()'

        p['title'] = response.xpath(title_xpath).get()
        p['IMDb_rating'] = response.xpath(score_xpath).get()
        p['popularity'] = response.xpath(popularity_xpath).get()
        p['genre'] = response.xpath(genres_xpath).getall()

        yield p