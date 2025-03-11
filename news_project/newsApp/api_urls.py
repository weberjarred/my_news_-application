"""
Maps API endpoints to views.

The RESTful API, as defined in the api_views.py file and mapped
within api_urls.py, provides endpoints that return articles
specifically tailored to the interests of readers based on their
subscriptions. This functionality ensures that third-party clients
receive only the most relevant data, enhancing user engagement and
satisfaction.


"""

from django.urls import path
from . import api_views
from .api_views import ArticleListCreateAPI


urlpatterns = [
    path(
        "articles/",
        api_views.ArticleListCreateAPI.as_view(),
        name="api_article_list"
    ),
]
