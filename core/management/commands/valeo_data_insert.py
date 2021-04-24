import json

from django.core.management import BaseCommand

from core.models import ValeoMapping


class Command(BaseCommand):

    def handle(self, *args, **options):
        parts = json.loads(open('valeo.json').read())
        objs = [ValeoMapping(**part) for part in parts]
        ValeoMapping.objects.bulk_create(objs)
