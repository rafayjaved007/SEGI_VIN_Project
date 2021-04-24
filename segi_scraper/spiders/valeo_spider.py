from scrapy import Request
from scrapy.link import Link
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_parameter, add_or_replace_parameter


class PaginationLE(object):
    def extract_links(self, response):
        page_no = url_query_parameter(response.url, 'page_no', None)
        if not response.css('.Result a'):
            return []

        return [Link(url=add_or_replace_parameter(response.url, 'page_no', int(page_no) + 1))]


class ValeoSpider(CrawlSpider):
    source = 'Valeo'
    name = 'valeo_spider'
    start_urls = ['http://www.valeocompressors.com/catalog/en/search.php?mode=0&page_no=1&proc=vehicle']
    rules = (Rule(PaginationLE()),
             Rule(LinkExtractor(restrict_css='.Result a'), callback='parse_part'),)

    def parse_part(self, response):
        refs = response.css('.textWeight:contains("Valeo Reference") + td::text').getall()
        item = {
            'make': response.css('.textWeight:contains("Make") + td::text').get().lower(),
            'model': response.css('.textWeight:contains("Model") + td::text').get().lower(),
            'year': int(response.css('.textWeight:contains("From YYYY-MM") + td::text').re_first(r'\d\d\d\d')),
            'link': response.url,
            'engine': int(response.css('.textWeight:contains("Engine Capacity") + td::text').get()),
            'engine_fuel': response.css('.textWeight:contains("Engine Fuel") + td::text').get(),
            'ref_new': response.css('.textWeight:contains("Valeo Reference (New)") + td::text').get(),
            'ref_reman': response.css('.textWeight:contains("Valeo Reference (Reman)") + td::text').get(),
            'ref_wo_clutch': refs[-2],
            'clutch_assembly': refs[-1],
            'source': self.source
        }
        return item

    def parse_image(self, response):
        image = response.css('')
