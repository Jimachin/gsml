import pickle
import datetime
import numpy as np
import pandas as pd
from django import forms
from .forms import EstimateForm
from django.shortcuts import render
from .models import Regression_ideal




def get_values(request):
    # if this is a POST request we need to process the form data
    context = {"rutPredictions": "12345678-k", "predictions": 0, "date_value": "mm/dd/yy"}
    if request.method == 'POST':
        form_view = EstimateForm(request.POST)
        print("POST")
        if form_view.is_valid():
            receptor_rut = form_view.cleaned_data["receptor_rut"]
            date_value = form_view.cleaned_data["date_value"]

            # query = get_object_or_404(Regression_ideal, receptor_rut=receptor_rut)

            try:
                query = Regression_ideal.objects.get(receptor_rut=receptor_rut)
                date_new_value = (pd.Timestamp(date_value, tz='UTC') - pd.Timestamp(query.date_min,
                                                                                    tz='UTC')) / np.timedelta64(1, 'D')

                with open(
                                        'C:/Users/Havy_DCC/Dropbox/Universidad/Python/PyCharm/Django/models/models/' + receptor_rut + '.pkl',
                        'rb') as f:
                    clf = pickle.load(f)
                    predictions = clf.predict(date_new_value)

                    print("Entro al post", date_value, receptor_rut, date_new_value)

                context = {"rutPredictions": query.receptor_rut, "predictions": np.round(predictions, 2)[0], "date_value": date_value,
                           'form_view': form_view}
                return render(request, 'estimate.html', context)
            except Regression_ideal.DoesNotExist:
                form_view.full_clean()
                raise forms.ValidationError("You have forgotten about Fred!")



    # if a GET (or any other method) we'll create a blank form
    else:
        form_view = EstimateForm()
        context = {"rutPredictions": "12345678-k", "predictions": 0.00, "date_value": " dd/mm/yy", 'form_view': form_view}
    return render(request, 'estimate.html', context)
