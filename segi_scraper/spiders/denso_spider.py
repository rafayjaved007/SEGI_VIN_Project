import scrapy
import requests
import json


class DensoSpider(scrapy.Spider):
    name = 'denso'
    start_urls = ['https://densoautoparts.com/find-my-part.aspx']

    year_make = {}

    make_model = {}
    model_engine = {}
    engine_dict = {}
    parts_dict = {}
    urls = {
            'make_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetMakes',
            'model_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetModels',
            'engine_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetEngines',
            'parts_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetParts'
        }

    def convert_to_json(self, url, dict):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://densoautoparts.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://densoautoparts.com/find-my-part.aspx',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        return json.loads(requests.post(url, json=dict, headers=headers).json()['d'])

    def parse(self, response):
        for year in range(2005, 2006):
            self.year_make.update({year: self.convert_to_json(url=self.urls['make_url'], dict={'Year': year})})
            for make in self.year_make[year]:
                self.make_model.update({make['Name']: self.convert_to_json(self.urls['model_url'], dict={'Year': year, 'Make': make['Id']})})
                for model in self.make_model[make['Name']]:
                    self.model_engine.update({model['Name']: self.convert_to_json(self.urls['engine_url'], dict={'BaseVehicleId': model['Id']})})
                    for engine in self.model_engine[model['Name']]:
                        self.parts_dict.update({engine['Id']: self.convert_to_json(self.urls['parts_url'], dict={
                                                                                                'BaseVehicleId': model['Id'],
                                                                                                'EngineBaseId': engine['Id'],
                                                                                                'Category': 'comp'})})
                        if self.parts_dict[engine['Id']]:
                            part_num = self.parts_dict[engine['Id']][0]['PartNumber']
                            img_url = f'https://densoimages.com/image/{part_num}/{part_num.split("-", 1)[1]}/'
                        else:
                            part_num, img_url = None, None

                        yield {
                             'year': year,
                             'make': make['Name'].lower(),
                             'model': model['Name'].lower(),
                             'engine': engine['Block'] + engine['Cylinders'] + ' ' + engine['Liter'] + engine['Block'],
                             'part_number': part_num,
                             'img_url': img_url
                        }
