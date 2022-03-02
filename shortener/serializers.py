import requests
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import Url, generate_hash
from rest_framework import serializers


class UrlSerializer(serializers.ModelSerializer):
    url_hash = serializers.CharField(
        max_length=100,
        label='Кастомная ссылка',
        required=False,
        validators=[UniqueValidator(queryset=Url.objects.all())],
        style={
            'placeholder': 'Необязательное поле'
        }
    )

    class Meta:
        model = Url
        fields = ('long_url', 'short_url', 'url_hash')
        extra_kwargs = {
            'long_url': {
                'validators': []
            },
            # 'url_hash': {
            #     'required': False
            # },
            'short_url': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        long_url = validated_data['long_url']
        url = Url.objects.filter(long_url=long_url)
        if url.exists():
            return url.first()
        if not (url_hash := validated_data.get('url_hash')):
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
        url_hash = attrs.get('url_hash')
        if url_hash and len(url_hash) < 7:
            raise ValidationError(
                {'url_hash': 'Идентификатор слишком короткий'}
            )
        return attrs
