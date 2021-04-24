import json

import bs4
import requests


class VIN:
    nhtsa_url_t = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/{vin}?format=json'
    vin_decoder_url_t = 'https://en.vindecoder.pl/{vin}'

    def lookup(self, vin):
        car_nhtsa = self.nhtsa_lookup(vin)
        if self.correct(car_nhtsa):
            return car_nhtsa, 'nhtsa'

        car_vindecoder = self.vin_decoder(vin)
        if self.correct(car_vindecoder):
            return car_vindecoder, 'vindecoder'

        return car_nhtsa, 'nhtsa'

    def nhtsa_lookup(self, vin):
        response = requests.get(self.nhtsa_url_t.format(vin=vin))
        car = {'vin': vin}

        for iteration in json.loads(response.text)['Results']:
            if iteration['Variable'] == 'Model Year':
                car['year'] = iteration['Value']
            if iteration['Variable'] == 'Model':
                car['model'] = iteration['Value']
            if iteration['Variable'] == 'Make':
                car['make'] = iteration['Value']
            if iteration['Variable'] == 'Displacement (L)':
                car['engine'] = f"{round(float(iteration['Value']), 1)}" + 'L' if iteration['Value'] else None

        return car

    def vin_decoder(self, vin):
        car = {'vin': vin}
        response = requests.get(self.vin_decoder_url_t.format(vin=vin))
        soup = bs4.BeautifulSoup(response.text, features="html.parser")

        for tr in soup.find_all('tr'):
            if not tr.th:
                continue

            if tr.th.text == 'Make':
                car['make'] = tr.td.text
            if tr.th.text == 'Model':
                car['model'] = tr.td.text
            if tr.th.text == 'Model year':
                car['year'] = tr.td.text
            if tr.th.text == 'Displacement Nominal':
                car['engine'] = tr.td.text+'L'

        return car

    def correct(self, car):
        if car.get('model') and car.get('year'):
            return True
        return False
