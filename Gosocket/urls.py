from rest_framework.authtoken import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/ml/get/', include("regression.api.urls", namespace="regressionApiUrl")),
    url(r'^estimate/', include("regression.urls", namespace="regressionEstimateUrl")),
    url(r'^token-auth/', views.obtain_auth_token, name="view_rest_framework_token")
]
