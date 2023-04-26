from rest_framework import serializers
from django.core.validators import URLValidator
from .models import Urls

class UrlsSerializer(serializers.ModelSerializer):
    custom_url_validator = URLValidator(schemes=['http', 'https'])
    url = serializers.URLField(validators=[custom_url_validator])

    class Meta:
        model = Urls
        fields = '__all__'

class TopUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = ('url', 'access_count')

class TopTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = ('url', 'title')
