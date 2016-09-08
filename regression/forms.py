from django import forms
from django.core import validators
from itertools import cycle
from .models import Regression_ideal


class EstimateForm(forms.Form):
    receptor_rut = forms.CharField(max_length=10)
    date_value = forms.DateField()

    def clean_receptor_rut(self):
        receptor_rut = self.cleaned_data['receptor_rut']
        query = Regression_ideal.objects.get(receptor_rut=receptor_rut)
        if not query.exist():
            raise forms.ValidationError("Rut not exist")
        return receptor_rut
