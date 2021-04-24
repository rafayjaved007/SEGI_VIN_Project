from django.core.management import BaseCommand

from core.utils import VIN

test_vins = [
    'WBAXC0109DDZ96933',
    '3C3CFFCR7FT580906',
    'WBA5A7100ED815564',
    'SAJAA18C3AMV07623',
    'WDBNF63J13A336717',
    'VF38D9HR8CL000635',
    'WBAFA110X4LT53603',
    'VF30U9HD8DS065602',
    'WVWZZZ13ZFV003961',
    'WBA3D3109CF242771',
    'WBAFR1109AC567B09',  # not in vindecoder
    'WBAHL83526DT01576',
    'WBAWZ5103F0L02786',
    'WBA3D3104EF895074',
    'WAUZZZ8K8FN024322',
    'WAUZZZ4F2AN015939',
    'YV1AS714081067294',
    'YV1AS982091093270',
    '1GBFH15T251143467',
    'JHLRE48507C210627',
    '1HGCM56344A141560',
]


class Command(BaseCommand):
    VIN = VIN()

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str)
        parser.add_argument('--vin', type=str)

    def handle(self, *args, **options):
        car = {}

        if options['source'] == 'nhtsa':
            car = self.VIN.nhtsa_lookup(options['vin'])
        elif options['source'] == 'vindecoder':
            car = self.VIN.vin_decoder(options['vin'])

        print(f"{options['source']} => {options['vin']}: {car}")

        # for vin in test_vins:
        #     car, source = self.VIN.lookup(vin)
        #     print(f'{source} => {vin}: {car}')
