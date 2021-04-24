from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from core.models import BAPMapping, Vehicle, ValeoMapping, DensoMapping


class VehicleAdmin(admin.ModelAdmin):
    model = Vehicle
    list_display = ('vin', 'year', 'make', 'model', 'engine')
    list_filter = ['year', 'make']
    search_fields = ['vin', 'year', 'make', 'model', 'engine']


class BAPMappingAdmin(admin.ModelAdmin):
    model = BAPMapping
    list_display = ('year', 'make', 'model', 'part', 'engine', 'link_to_part_number', 'inventory')
    list_filter = ['year', 'make']
    search_fields = ['year', 'make', 'model', 'engine', 'part_number']

    def link_to_part_number(self, obj):
        html = ''
        for part_number in obj.part_number.split(' | '):
            html += f'<a href="https://www.google.com/search?q={part_number}&tbm=isch" target="_blank">{part_number}</a> | '
        return format_html(html[:-2])


class ValeoAdmin(admin.ModelAdmin):
    model = ValeoMapping
    list_display = ('year', 'make', 'model',  'engine',  'ref_new', # 'part',
                    'ref_reman', 'ref_wo_clutch', 'clutch_assembly', 'inventory')
    list_filter = ['year', 'make']
    search_fields = ['year', 'make', 'model', 'engine', 'ref_new', 'ref_reman', 'ref_wo_clutch', 'clutch_assembly']

    # def link_to_part_number(self, obj):
    #     html = ''
    #     for part_number in obj.part_number.split(' | '):
    #         html += f'<a href="https://www.google.com/search?q={part_number}&tbm=isch" target="_blank">{part_number}</a> | '
    #     return format_html(html[:-2])


class DensoAdmin(admin.ModelAdmin):
    model = DensoMapping
    list_display = ('year', 'make', 'model',  'engine', 'part_number', 'link_to_img',)
    list_filter = ['year', 'make']
    search_fields = ['year', 'make', 'model', 'engine', 'part_number']

    def link_to_img(self, obj):
        html = ''
        for part_number in obj.part_number.split(' | '):
            html += f'<a href="{obj.image_url}" target="_blank">{part_number}</a> | '
        return format_html(html[:-2])


admin.site.register(BAPMapping, BAPMappingAdmin)
admin.site.register(ValeoMapping, ValeoAdmin)
admin.site.register(DensoMapping, DensoAdmin)
admin.site.register(Vehicle, VehicleAdmin)
