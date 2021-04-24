import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from core.models import BAPMapping


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int)

    def handle(self, *args, **options):
        for part in BAPMapping.objects.filter(year=options['year']).exclude(part_number__contains='|'):
            response = requests.get(part.link)
            html = BeautifulSoup(response.text)
            all_part_numbers = {elem.text for elem in html.find_all('span', {'id': 'fits_oem'})}
            part.part_number = ' | '.join(all_part_numbers)
            part.save()
