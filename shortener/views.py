from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from urllib.parse import unquote

from .models import Urls
from .serializers import TopUrlsSerializer, UrlsSerializer,TopTitleSerializer
from .utils import base62_encode
from .tasks import fetch_and_store_title

class ShortenerView(GenericAPIView):
    serializer_class = UrlsSerializer

    def get(self, request, url):
        decoded_url = unquote(url)
        serializer = UrlsSerializer(data={'url': decoded_url})
        if serializer.is_valid():
            url_shortened, created = Urls.objects.get_or_create(url=decoded_url)
            if created:
                url_shortened.shortened_url_id = base62_encode(url_shortened.id)
                url_shortened.save()
            # Process the URL and return a response
            fetch_and_store_title.delay(url_shortened.shortened_url_id)
            shortened_path = f'/url/{url_shortened.shortened_url_id}/'
            shortened_url = request.build_absolute_uri(shortened_path)
            return Response({'shortened_url': shortened_url})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            ...

class RedirectUrlView(GenericAPIView):
    serializer_class = UrlsSerializer

    def get(self, request, id):
        short_url_obj = get_object_or_404(Urls, shortened_url_id=id)
        short_url_obj.access_count += 1  # Increment access count
        short_url_obj.save()
        return redirect(short_url_obj.url)

class TopUrlsView(GenericAPIView):
    serializer_class = TopUrlsSerializer

    def get(self, request):
        top_100_urls = Urls.objects.order_by('-access_count')[:100]
        serializer = TopUrlsSerializer(top_100_urls, many=True)
        return Response(serializer.data)

class TopTitlesView(GenericAPIView):
    serializer_class = TopTitleSerializer

    def get(self, request):
        top_100_urls = Urls.objects.order_by('-access_count')[:100]
        serializer = TopTitleSerializer(top_100_urls, many=True)
        return Response(serializer.data)

