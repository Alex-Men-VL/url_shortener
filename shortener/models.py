import base64
import os
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_hash():
    while True:
        url_hash_bytes = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:7]
        url_hash = url_hash_bytes.decode('utf-8')

        url_hash_exist = Url.objects.filter(url_hash=url_hash).exists()
        if not url_hash_exist:
            return url_hash


class Url(models.Model):
    long_url = models.URLField(
        'исходный URL',
        db_index=True,
        unique=True
    )
    url_hash = models.CharField(
        'идентификатор',
        max_length=100,
        unique=True,
    )
    short_url = models.URLField(
        'сокращенный URl',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        'время создания',
        default=timezone.now
    )

    def create_short_url(self):
        short_url = os.path.join(settings.HOST_NAME, self.url_hash)
        self.short_url = short_url
        return self.save()

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def __str__(self):
        return self.url_hash
