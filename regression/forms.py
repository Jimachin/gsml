from django import forms
from django.core import validators
from itertools import cycle


class EstimateForm(forms.Form):
    receptor_rut = forms.CharField(max_length=10, validators=[validators.validate_slug])
    date_value = forms.DateField()

    def clean_receptor_rut(self):
        receptor_rut = self.cleaned_data['receptor_rut']
        reversed_digits = map(int, reversed(str(receptor_rut)))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_digits, factors))

        return (-s) % 11