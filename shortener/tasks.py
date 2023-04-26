import requests
from bs4 import BeautifulSoup

from celery import shared_task
from .models import Urls

@shared_task
def fetch_and_store_title(shortened_url_id):
    url_obj = Urls.objects.get(shortened_url_id=shortened_url_id)
    url = url_obj.url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else ''

    url_obj.title = title
    url_obj.save()
