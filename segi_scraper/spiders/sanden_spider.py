import scrapy
import requests
import json


class SandenSpider(scrapy.Spider):
    name = 'sanden'
    start_urls = ['https://www.sanden.com']
    make_dict = []

    def parse(self, response, **kwargs):
        value = response.xpath('//select[contains(@name, "make")]/option/@value').extract()
        make = response.xpath('//select[contains(@name, "make")]/option/text()').extract()
        for make, value in zip(make, value):
            if value != '':
                self.make_dict.append({'Value': value, 'Name': make})

        return self.parse_items(self.make_dict)

    def get_list(self, find, value):
        if value != '':
            return json.loads(requests.get(url=f'https://www.sanden.com/common/script/aftermarket-process.php?f={find}&_value={value}').text.replace("\'", "\""))

    def parse_items(self, make_dict):
        for make in make_dict:
            model_list = json.loads(requests.get(url=f'https://www.sanden.com/common/script/aftermarket-process.php?f=model&_value={make["Value"]}').text.replace("\'", "\""))
            for model_dict in model_list:
                model_value, model_name = list(model_dict.keys())[0], list(model_dict.values())[0]
                if model_value != '':
                    for engine_dict in self.get_list('engine', model_value):
                        engine_value, engine_name = list(engine_dict.keys())[0], list(engine_dict.values())[0]
                        if engine_value != '':
                            for year_dict in self.get_list('year', engine_value):
                                year_value, year = list(year_dict.keys())[0], list(year_dict.values())[0]
                                if year_value != '':
                                    for part_dict in self.get_list('part', year_value):
                                        part_value, part_num = list(part_dict.keys())[0], list(part_dict.values())[0]
                                        if part_value != '':
                                            yield {
                                                'make': make['Name'].lower(),
                                                'model': model_name.lower(),
                                                'engine': engine_name,
                                                'year': year,
                                                'part_num': part_num,
                                                'url': f'https://www.sanden.com/product.php?model={part_num}',
                                                'image_url': f'https://www.sanden.com/productlibrary/photos/{part_num}.jpg'
                                            }
