import json

import bs4
import requests


# Function to get proxies
from core.utils import VIN


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs4.BeautifulSoup(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


class PartNumber:

    # Hard Coded car details for testing
    car_details = {
        'Model Year': 2005,
        'Model': 'Ascender',
        'Make': 'Isuzu',
        'Engine': None
    }
    # Car data from website
    # car_details = vin_dec_lookup('KM8J33A22HU273373')
    urls = {
        'make_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetMakes',
        'model_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetModels',
        'engine_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetEngines',
        'parts_url': 'https://densoautoparts.com/feeds/feeds.asmx/DENSO_GetParts'
    }
    data_dict = {"Year": car_details['Model Year']}

    def convert_to_json(self, url, dict):
        headers1 = {
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
            'Cookie': 'ASP.NET_SessionId=lczxy4nbkipeuy45r0s3june; _gcl_au=1.1.1142732189.1597336159; _ga=GA1.2.370697867.1597336159; _gid=GA1.2.1569653375.1597336159; _fbp=fb.1.1597336159994.1681595523; __qca=P0-380654197-1597336159759; .ASPXANONYMOUS=9FXcLiSo1gEkAAAANWUzODFlOGYtOTc0MC00MzIyLWE4NmMtMGM3ZjgwODA2NmU4nxIxR5uiPqNjbANDH4VJ8YV63-k1; _gat_UA-2602407-25=1'

        }
        res = requests.post(url, json=dict, headers=headers1).json()
        return json.loads(res['d'])

    def fetch_id(self, data_dict, url, match):
        req_dict = self.convert_to_json(url, data_dict)
        for req_data in req_dict:
            if req_data['Name'] == self.car_details[f'{match}']:
                return req_data['Id']

    def fetch_make_id(self):
        self.data_dict.update({'Make': self.fetch_id(data_dict=self.data_dict, url=self.urls['make_url'], match='Make')})
        return self.data_dict

    def fetch_model_id(self, dict):
        dict.update({'BaseVehicleId': self.fetch_id(data_dict=dict, url=self.urls['model_url'], match='Model')})
        return dict

    def fetch_engine_id(self, dict):
        engine_dict = self.convert_to_json(self.urls['engine_url'], self.data_dict)
        dict.update({'EngineBaseId': engine_dict[0]['Id']})
        return dict

    def fetch_part_num(self, dict):
        parts_dict = {
            'EngineBaseId': dict['EngineBaseId'],
            'BaseVehicleId': dict['BaseVehicleId'],
            'Category': 'comp'
        }
        part_dict = self.convert_to_json(self.urls['parts_url'], parts_dict)
        return part_dict[0]['PartNumber']

# Getting make id by posting year
dict = PartNumber().fetch_make_id()
# Getting BaseVehicleId by posting Year and make id
final_dict = PartNumber().fetch_model_id(dict)
# Getting Engine Id by posting BaseVehicleId
parts_dict = PartNumber().fetch_engine_id(final_dict)
# Getting part number by posting EngineId, BaseVehicleId and category as comp for A/C compressor
print(PartNumber().fetch_part_num(parts_dict))


