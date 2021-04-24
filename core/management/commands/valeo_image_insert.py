import json

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from core.models import ValeoMapping


class Command(BaseCommand):

    def handle(self, *args, **options):
        for part in ValeoMapping.objects.all():
            ref = part.ref_new
            url = self.acpart(ref)
            print(url)
        # url = self.acpart('5062118730')

    def acpart(self, ref):
        search_term = ref[:6] + '-' + ref[-4:]
        url = f'https://www.acparts.com/?s={search_term}&post_type=product'
        soup = BeautifulSoup(requests.get(url).text, features="html.parser")
        img = soup.find('img', {'class': 'wp-post-image'})
        return img['data-large_image'] if img else None
