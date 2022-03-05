from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import Url


class TestCreateShortURLAPIView(APITestCase):

    def test_correct_long_url(self):
        short_url_count = Url.objects.count()
        payload = {'long_url': 'https://www.djangoproject.com/'}
        response = self.client.post(
            reverse('create_short_link_api-list'),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        short_url_response = self.client.get(response.data['short_url'])
        self.assertEqual(short_url_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(short_url_count+1, Url.objects.count())

    def test_correct_long_url_and_url_hash(self):
        payload = {'long_url': 'https://www.djangoproject.com/start/',
                   'url_hash': 'django_start_page'}
        response = self.client.post(
            reverse('create_short_link_api-list'),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['url_hash'], payload['url_hash'])

        short_url_response = self.client.get(response.data['short_url'])
        self.assertEqual(short_url_response.status_code, status.HTTP_302_FOUND)

    def test_incorrect_long_url(self):
        payload = {'long_url': 'https://www.djangoproject.com/incorrect_path'}
        response = self.client.post(
            reverse('create_short_link_api-list'),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['long_url'][0], 'Некорректная ссылка')

    def test_short_url_hash(self):
        payload = {
            'long_url': 'https://www.djangoproject.com/start/overview/',
            'url_hash': 'django'
        }
        response = self.client.post(
            reverse('create_short_link_api-list'),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['url_hash'][0],
                         'Идентификатор слишком короткий')


class TestCreateShortURLView(TestCase):

    def test_get_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response,
                                'create_short_link.html')

    def test_correct_long_url(self):
        payload = {'long_url': 'https://docs.djangoproject.com/en/4.0/'}
        response = self.client.post('/', payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        short_url_response = self.client.get(
            response.data['serializer'].data['short_url']
        )
        self.assertEqual(short_url_response.status_code, HTTPStatus.FOUND)

    def test_correct_long_url_with_url_hash(self):
        payload = {'long_url': 'https://www.djangoproject.com/weblog/',
                   'url_hash': 'django_weblog'}
        response = self.client.post('/', payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['serializer'].data['url_hash'],
                         payload['url_hash'])

        short_url_response = self.client.get(
            response.data['serializer'].data['short_url']
        )
        self.assertEqual(short_url_response.status_code, HTTPStatus.FOUND)

    def test_incorrect_long_url(self):
        payload = {'long_url': 'https://www.djangoproject.com/incorrect_path'}
        response = self.client.post('/', payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Некорректная ссылка', html=True)

    def test_short_url_hash(self):
        payload = {
            'long_url': 'https://www.djangoproject.com/start/overview/',
            'url_hash': 'django'
        }
        response = self.client.post('/', payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,
                            'Идентификатор слишком короткий',
                            html=True)
