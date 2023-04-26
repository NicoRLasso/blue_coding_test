import unittest
from urllib.parse import quote
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from unittest import mock

from .utils import base62_encode
from .tasks import fetch_and_store_title
from .models import Urls
from .serializers import UrlsSerializer, TopUrlsSerializer, TopTitleSerializer

class UrlsModelTestCase(TestCase):
    def setUp(self):
        Urls.objects.create(
            url="https://www.example.com",
            title="Example",
            access_count=0
        )

    def test_urls_model(self):
        url = Urls.objects.get(title="Example")
        self.assertEqual(url.url, "https://www.example.com")
        self.assertEqual(url.title, "Example")
        self.assertEqual(url.access_count, 0)
        self.assertEqual(str(url), "https://www.example.com")

class UrlsSerializerTestCase(TestCase):
    def setUp(self):
        self.url = Urls.objects.create(
            url="https://www.example.com",
            title="Example",
            access_count=0
        )
        self.serializer = UrlsSerializer(instance=self.url)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'url', 'shortened_url_id', 'title', 'access_count'])

class TopUrlsSerializerTestCase(TestCase):
    def setUp(self):
        self.url = Urls.objects.create(
            url="https://www.example.com",
            title="Example",
            access_count=0
        )
        self.serializer = TopUrlsSerializer(instance=self.url)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['url', 'access_count'])

class TopTitleSerializerTestCase(TestCase):
    def setUp(self):
        self.url = Urls.objects.create(
            url="https://www.example.com",
            title="Example",
            access_count=0
        )
        self.serializer = TopTitleSerializer(instance=self.url)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['url', 'title'])

class FetchAndStoreTitleTaskTestCase(TestCase):
    def setUp(self):
        self.url_obj = Urls.objects.create(
            url='http://www.example.com',
            shortened_url_id=1
        )

    @mock.patch('requests.get')
    def test_fetch_and_store_title(self, mock_get):
        # Set up the mock response
        mock_response = mock.MagicMock()
        mock_response.content = '<html><head><title>Example Page</title></head></html>'
        mock_get.return_value = mock_response

        # Call the task
        fetch_and_store_title(shortened_url_id=1)

        # Check that the title was stored correctly
        url_obj = Urls.objects.get(shortened_url_id=1)
        self.assertEqual(url_obj.title, 'Example Page')

class Base62EncodeTestCase(unittest.TestCase):
    def test_base62_encode(self):
        self.assertEqual(base62_encode(0), '0')
        self.assertEqual(base62_encode(1), '1')
        self.assertEqual(base62_encode(61), 'Z')
        self.assertEqual(base62_encode(62), '10')
        self.assertEqual(base62_encode(3844), '100')
        self.assertEqual(base62_encode(238327), 'ZZZ')

class ShortenerViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://www.example.com'

    @mock.patch('shortener.views.fetch_and_store_title.delay')
    def test_shortener_view(self, mock_fetch_and_store_title):
        # Test a valid request
        response = self.client.get(f'/shorten/?url={quote(self.url)}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['shortened_url'], '/url/1/')
        self.assertEqual(Urls.objects.count(), 1)

        # Test a request with an invalid URL
        response = self.client.get(f'/shorten/?url=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Urls.objects.count(), 1)

class RedirectUrlViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = Urls.objects.create(
            url='http://www.example.com',
            shortened_url_id='1'
        )

    def test_redirect_url_view(self):
        # Test a valid request
        response = self.client.get(f'/url/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://www.example.com')
        self.assertEqual(Urls.objects.first().access_count, 1)

        # Test a request with an invalid URL ID
        response = self.client.get(f'/url/invalid/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Urls.objects.first().access_count, 1)

class TopUrlsViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.urls = [
            Urls.objects.create(url=f'http://www.example{i}.com', access_count=i)
            for i in range(1, 4)
        ]

    def test_top_urls_view(self):
        response = self.client.get('/top/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data,
            TopUrlsSerializer(Urls.objects.order_by('-access_count'), many=True).data
        )

