import scrapy

## Scraping links to movies to list
class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListSpider(scrapy.Spider):
    name = 'link_list'
    allowed_domains = ['https://www.imdb.com/']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):
        xpath = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr/td[1]//@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.imdb.com/' + s.get()
            yield l