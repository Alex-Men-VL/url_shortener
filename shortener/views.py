from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from .models import Url
from .serializers import UrlSerializer


class CreateShortURL(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


class RedirectShortUrl(APIView):
    def get(self, request, url_hash):
        url = get_object_or_404(Url, url_hash=url_hash)
        long_url = url.long_url
        return HttpResponseRedirect(long_url)

