import pickle
import datetime
import numpy as np
import pandas as pd

from rest_framework.serializers import (HyperlinkedIdentityField, ModelSerializer, SerializerMethodField,
                                        ValidationError)

from Gosocket.settings import MODELS_PATH
from regression.models import Regression_ideal

# this is to put hyperlink , instead of each value
# <'regression_API' is the name of regression.api.urls>:<name of the view that you want to see>
urlHyperlink = HyperlinkedIdentityField(
    view_name='regressionApiUrl:PredictionApiRutIdealView',
    lookup_field='receptor_rut'
)


class RegressionListAllSerializer(ModelSerializer):
    url = urlHyperlink

    class Meta:
        model = Regression_ideal
        fields = ('receptor_rut', 'url')


class RegressionPredictionsSerializer(ModelSerializer):
    predictions = SerializerMethodField()
    product_code = SerializerMethodField()
    product_name = SerializerMethodField()

    class Meta:
        model = Regression_ideal
        fields = ('receptor_rut', 'product_code', 'product_name', 'predictions')

    def get_predictions(self, obj):
        date_value = datetime.datetime.now().date()

        date_new_value = (pd.Timestamp(date_value, tz='UTC') - pd.Timestamp(obj.date_min, tz='UTC')) / np.timedelta64(1,
                                                                                                                      'D')

        with open(MODELS_PATH + obj.receptor_rut + '.pkl', 'rb') as f:
            clf_Text = pickle.load(f)
            predictions = clf_Text.predict(date_new_value)

        return predictions[0]

    def get_product_code(self, obj):
        product_code = 23633
        return product_code

    def get_product_name(self, obj):
        product_name = "Pan Blanco Artesanal 600g"
        return product_name
