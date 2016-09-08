from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views
from django.conf.urls import include, url
from django.contrib import admin

from Gosocket import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/ml/get/', include("regression.api.urls", namespace="regressionApiUrl")),
    url(r'^estimate/', include("regression.urls", namespace="regressionEstimateUrl")),
    url(r'^token-auth/', views.obtain_auth_token, name="view_rest_framework_token")
]


# puts the static files in development mode
urlpatterns += staticfiles_urlpatterns()

# put the media files in development mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)