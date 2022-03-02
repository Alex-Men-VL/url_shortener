from rest_framework import viewsets, mixins

from .models import Url
from .serializers import UrlSerializer


class CreateShortURL(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
