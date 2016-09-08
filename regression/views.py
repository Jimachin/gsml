import pickle
import logging
import numpy as np
import pandas as pd
from django import forms
import locale
from Gosocket import settings
from .forms import EstimateForm
from django.shortcuts import render
from .models import Regression_ideal

logger = logging.getLogger(__name__)


def get_values(request):
    # locale.setlocale(locale.LC_NUMERIC, 'es_ES.utf-8')
    locale.setlocale(locale.LC_ALL, locale="es")
    try:
        # if this is a POST request we need to process the form data
        context = {"rutPredictions": "12345678-k", "predictions": 0, "date_value": "mm/dd/yy"}
        if request.method == 'POST':
            form_view = EstimateForm(request.POST)

            if form_view.is_valid():

                receptor_rut = form_view.cleaned_data["receptor_rut"]
                date_value = form_view.cleaned_data["date_value"]

                # query = get_object_or_404(Regression_ideal, receptor_rut=receptor_rut)

                try:
                    query = Regression_ideal.objects.get(receptor_rut=receptor_rut)
                    date_new_value = (pd.Timestamp(date_value, tz='UTC') - pd.Timestamp(query.date_min,
                                                                                        tz='UTC')) / np.timedelta64(1,
                                                                                                                    'D')
                    with open(settings.MODELS_PATH + receptor_rut + '.pkl', 'rb') as f:
                        clf = pickle.load(f)
                        predictions = np.round(clf.predict(date_new_value), 0)[0]

                        print("Entro al post", date_value, receptor_rut, date_new_value)

                    context = {"rutPredictions": query.receptor_rut,
                               # "predictions": locale.format("%.*f", (0, predictions), True),
                               "predictions": locale.format("%d", predictions, grouping=True),
                               "date_value": date_value, 'form_view': form_view}
                    return render(request, 'estimate.html', context)

                except Regression_ideal.DoesNotExist:
                    form_view.full_clean()
                    raise forms.ValidationError("You have forgotten about Fred!")

        # if a GET (or any other method) we'll create a blank form
        else:
            form_view = EstimateForm()
            context = {"rutPredictions": "12345678-k", "predictions": 0.00, "date_value": " dd/mm/yy",
                       'form_view': form_view}
        return render(request, 'estimate.html', context)

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise exc
