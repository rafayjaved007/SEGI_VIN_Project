import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.db.models import Q
from django.views.generic import FormView, TemplateView

from core.forms import VINForm
from core.models import BAPMapping, Vehicle, ValeoMapping
from core.utils import VIN


class HomeView(LoginRequiredMixin, FormView):
    template_name = 'core/home.html'
    form_class = VINForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        vin = request.POST['search_box']
        saved_vins = Vehicle.objects.filter(vin=vin)
        if saved_vins.exists():
            vehicle, source = saved_vins.values()[0], 'Database'
        else:
            vehicle, source = VIN().lookup(vin)
            Vehicle(**vehicle).save()

        bapparts = self.fetch_parts(vehicle, BAPMapping)
        valeoparts = self.fetch_parts(vehicle, ValeoMapping)

        for part in bapparts:
            if '|' not in part.part_number:
                response = requests.get(part.link)
                html = BeautifulSoup(response.text)
                all_part_numbers = {elem.text for elem in html.find_all('span', {'id': 'fits_oem'})}
                part.part_number = ' | '.join(all_part_numbers)
                part.save()

        bapparts = bapparts.values()
        for part in bapparts:
            part['part_numbers'] = part['part_number'].split(' | ')

        self.extra_context = {'vehicle': vehicle, 'source': source,
                              'bapparts': bapparts, 'valeoparts': valeoparts}

        return super().get(request)

    def fetch_parts(self, vehicle, Model):
        parts = Model.objects.filter(year=vehicle['year'], make=vehicle['make'].lower())

        if parts and vehicle.get('model'):
            parts = parts.filter(
                Q(model__in=vehicle['model']) | Q(model=vehicle['model']) | Q(model__contains=vehicle['model'])
            )

        if parts and vehicle.get('engine'):
            temp = parts.filter(
                Q(engine__in=vehicle['engine']) | Q(engine=vehicle['engine']) | Q(engine__contains=vehicle['engine'])
            )
            parts = temp if temp else parts

        return parts

        # return HttpResponseRedirect(f'{reverse("results")}?vin={vin}')

#
# class ResultView(LoginRequiredMixin, TemplateView):
#     template_name = 'core/result.html'
#     extra_context = {
#         'part_code': None
#     }
#
#     def get(self, request, *args, **kwargs):
#         vin = request.GET['vin']
#         self.extra_context['part_code'] = 'something'
#         return super().get(request)
