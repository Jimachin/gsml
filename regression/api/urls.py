from django.conf.urls import url
from regression.api.views import PredictionApiAllIdealView, PredictionApiRutIdealView

urlpatterns = [
    url(r'^$', PredictionApiAllIdealView.as_view(), name='PredictionApiAllIdealView'),
    url(r'^(?P<receptor_rut>[\w-]+)/$', PredictionApiRutIdealView.as_view(), name='PredictionApiRutIdealView'),
]
