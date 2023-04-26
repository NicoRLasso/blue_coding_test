from django.urls import path, re_path
from .views import ShortenerView, RedirectUrlView, TopUrlsView,TopTitlesView

urlpatterns = [
    re_path(r'^shorten/(?P<url>.+)/$', ShortenerView.as_view(), name='shortener'),
    path('url/<str:id>/', RedirectUrlView.as_view(), name='redirect_url'),
    path('top-urls/', TopUrlsView.as_view(), name='top_urls'),
    path('top-titles/', TopTitlesView.as_view(), name='top_titles'),
]
