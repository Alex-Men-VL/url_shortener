from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Url
from .serializers import UrlSerializer


class CreateShortURLAPI(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


class CreateShortURL(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'create_short_link.html'

    def get(self, request):
        serializer = UrlSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UrlSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        short_url = serializer.data.get('short_url')
        return Response({'serializer': serializer, 'short_url': short_url})


class RedirectShortUrl(APIView):
    def get(self, request, url_hash):
        url = get_object_or_404(Url, url_hash=url_hash)
        long_url = url.long_url
        return HttpResponseRedirect(long_url)

