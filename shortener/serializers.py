import requests
from rest_framework.exceptions import ValidationError

from .models import Url, generate_hash
from rest_framework import serializers


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('long_url', 'short_url')
        read_only_fields = ('short_url',)
        extra_kwargs = {
            'long_url': {
                'validators': []
            }
        }

    def create(self, validated_data):
        long_url = validated_data['long_url']
        url = Url.objects.filter(long_url=long_url)
        if url.exists():
            return url.first()
        url_hash = generate_hash()
        url = Url.objects.create(long_url=long_url, url_hash=url_hash)
        url.create_short_url()
        return url

    def validate(self, attrs):
        long_url = attrs['long_url']
        response = requests.get(long_url)
        if not response.ok:
            raise ValidationError(
                {'long_url': 'Некорректная ссылка'}
            )
        return attrs
