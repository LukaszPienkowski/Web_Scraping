import scrapy

limit_100_pages = True
#limit_100_pages = False

class Movie(scrapy.Item):
    title = scrapy.Field()
    IMDb_rating = scrapy.Field()
    popularity = scrapy.Field()
    genre = scrapy.Field()

## This spider scraps data for each movie (title, score, popularity, genres) and saves it to csv file
class LinksSpider(scrapy.Spider):
    name = 'movie_scraper'
    allowed_domains = ['https://www.imdb.com/']
    try:
        with open("link_list.csv", "rt") as f:
            if limit_100_pages:
                start_urls = [url.strip() for url in f.readlines()][1:102]
            else:
                start_urls = [url.strip() for url in f.readlines()]
    except:
        start_urls = []

    def parse(self, response, **kwargs):
        p = Movie()

        title_xpath = '//h1/text()'
        score_xpath = '//div[@data-testid = "hero-rating-bar__aggregate-rating__score"]/span/text()'
        popularity_xpath = '//div[@data-testid = "hero-rating-bar__popularity__score"]/text()'
        genres_xpath = '//div[@data-testid = "genres"]//text()'

        p['title'] = response.xpath(title_xpath).get()
        p['IMDb_rating'] = response.xpath(score_xpath).get()
        p['popularity'] = response.xpath(popularity_xpath).get()
        p['genre'] = response.xpath(genres_xpath).getall()
        #p['genre'] = [w.replace("\n", ',') for w in p['genre']]

        yield p