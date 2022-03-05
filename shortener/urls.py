from django.urls import path, include
from rest_framework import routers

from .views import CreateShortURLAPI, CreateShortURL, RedirectShortUrl

router = routers.DefaultRouter()
router.register(r'create', CreateShortURLAPI, basename='create_short_link_api')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', CreateShortURL.as_view(), name='create_short_link'),
    path('<str:url_hash>', RedirectShortUrl.as_view(),
         name='long_url_redirect'),
]
