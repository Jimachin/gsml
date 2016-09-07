from django.conf.urls import url
from .views import get_values

urlpatterns = [
    # url(regex=r'^((?P<receptor_rut>[0-9]+)/)?$', view=Estimate_view.as_view(), name='view_estimateRegression'),
    # url(regex=r'', view=get_Estimate_view, name='view_estimateRegression'),
    url(regex=r'', view=get_values, name='view_estimateRegression'),
]
