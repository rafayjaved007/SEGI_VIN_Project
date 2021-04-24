from django import forms


class VINForm(forms.Form):
    search_box = forms.CharField(label='VIN', max_length=17)
