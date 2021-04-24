import json
import requests

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


def convert_to_json(url, dict):
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


# Following range is for testing purpose. Range to get all data is from 1946 to 2021
for year in range(2005, 2006):
    year_make.update({year: convert_to_json(urls['make_url'], dict={'Year': year})})
    for make in year_make[year]:
        make_model.update({make['Name']: convert_to_json(urls['model_url'], dict={'Year': year, 'Make': make['Id']})})
        for model in make_model[make['Name']]:
            model_engine.update({model['Name']: convert_to_json(urls['engine_url'], dict={'BaseVehicleId': model['Id']})})
            for engine in model_engine[model['Name']]:
                parts_dict.update({engine['Id']: convert_to_json(urls['parts_url'], dict={
                                                                                        'BaseVehicleId': model['Id'],
                                                                                        'EngineBaseId': engine['Id'],
                                                                                        'Category': 'comp'})})

print(parts_dict)
# # Key=year & value=make
# print(year_make)
# # Key=make & value=model
# print(make_model)
# # Key=model & value=engine
# print(model_engine)
# # Key=engine id & value=part
# print(engine_part475