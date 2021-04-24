import json

from django.core.management import BaseCommand

from core.models import DensoMapping


class Command(BaseCommand):

    def handle(self, *args, **options):
        parts = json.loads(open('denso.json').read())
        missing_part_numbers = []
        objs = []
        for part in parts:
            if part['part_number']:
                part['image_url'] = part.pop('img_url')
                objs.append(DensoMapping(**part))
            else:
                missing_part_numbers.append(part)
        # DensoMapping.objects.bulk_create(objs)
        with open('denso_missing_part_number.json', 'w') as file:
            file.writelines(json.dumps(missing_part_numbers, indent=4))
