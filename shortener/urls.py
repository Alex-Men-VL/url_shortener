from django.urls import path, include
from rest_framework import routers

from .views import CreateShortURL, RedirectShortUrl

router = routers.DefaultRouter()
router.register(r'create', CreateShortURL)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('<str:url_hash>', RedirectShortUrl.as_view())
]
