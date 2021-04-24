import json
import re

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from w3lib.url import add_or_replace_parameters

from core.models import BAPMapping

headers = {
    'authority': 'www.buyautoparts.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.buyautoparts.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.buyautoparts.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

errors_lookups = []


def fill_table(link, fitment=None):
    link_parts = link.replace('_', ' ').split('/')
    try:
        obj = {
            'year': int(link_parts[4]),
            'make': link_parts[5],
            'model': link_parts[6],
            'part': link_parts[7],
            'part_number': link_parts[8],
            'fitment': fitment,
            'link': link
        }
        obj = BAPMapping.objects.create(**obj)
        obj.save()
    except Exception as e:
        print(link)


def current(lookup, final_dictionary):
    current_pointer = final_dictionary
    if 'year' in lookup:
        current_pointer = current_pointer[lookup['year']]['Childs']

    if 'make' in lookup:
        current_pointer = current_pointer[lookup['make']]['Childs']

    if 'model' in lookup:
        current_pointer = current_pointer[lookup['model']]['Childs']

    if 'partname' in lookup:
        current_pointer = current_pointer[lookup['partname']]['Childs']

    if 'cnsuffix' in lookup:
        current_pointer = current_pointer[lookup['cnsuffix']]['Childs']

    return current_pointer


def get_dict(lookup, final_dictionary):
    url = add_or_replace_parameters('https://www.buyautoparts.com/partsearch/homegetymmdetails.asp', lookup)
    soup = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser")

    options = soup.find_all('option')
    current_dict = current(lookup, final_dictionary)
    if options:
        reqmake = re.findall(r"var reqmake =  '(.*)'", soup.find('script').string)
        for option in options:
            value = option.get('value')
            if value:
                current_dict[value] = {'Name': option.text, 'Childs': {}}
                yield value, reqmake[0] if reqmake else None
    else:
        try:
            current_dict['Link'] = re.findall(r"0 ~(.*)~", soup.text)[0]
            fill_table(current_dict['Link'])
        except Exception as e:
            errors_lookups.append(lookup)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int)

    def handle(self, *args, **options):
        final_dictionary = {}

        for year in range(options['year'], options['year'] + 1):
            final_dictionary[year] = {'Name': year, 'Childs': {}}
            year_lookup = {'year': year}

            for make_id, _ in get_dict(year_lookup, final_dictionary):
                make_lookup = year_lookup.copy()
                make_lookup['make'] = make_id

                for model_id, _ in get_dict(make_lookup, final_dictionary):
                    model_lookup = make_lookup.copy()
                    model_lookup['model'] = model_id

                    for part_id, _ in get_dict(model_lookup, final_dictionary):
                        part_lookup = model_lookup.copy()
                        part_lookup['partname'] = part_id
                        part_lookup['part'] = part_id[:4]

                        for fitment_id, make in get_dict(part_lookup, final_dictionary):
                            nav_lookup = part_lookup.copy()
                            nav_lookup['cnsuffix'] = fitment_id

                            fitment_lookup = part_lookup.copy()
                            fitment_lookup.pop('part')
                            fitment_lookup['make'] = make
                            fitment_lookup['cnsuffix'] = fitment_id

                            url = add_or_replace_parameters('https://www.buyautoparts.com/partsearch/newfitmentajax.asp', fitment_lookup)
                            soup = BeautifulSoup(requests.get(url, headers=headers).text, features="html.parser")

                            current_dict = current(nav_lookup, final_dictionary)
                            try:
                                current_dict['Link'] = soup.text
                                fill_table(current_dict['Link'], fitment_id)
                            except Exception as e:
                                errors_lookups.append(nav_lookup)
        if errors_lookups:
            json_text = json.dumps(errors_lookups, indent=4)
            print(json_text)
            with open('error_lookups.json', 'w') as error_file:
                error_file.writelines(json_text)
