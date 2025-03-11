"""
This file contains the URL patterns defined for the web views.
"""

from django.urls import path
from . import views


urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("article/create/", views.article_create, name="article_create"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("article/approval/", views.article_approval, name="article_approval"),
    path("article/<int:pk>/delete/", views.article_delete, name="article_delete"),
    path(
        "subscribe/<int:journalist_id>/",
        views.subscribe_journalist,
        name="subscribe_journalist",
    ),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path(
        "journalist/<int:journalist_id>/",
        views.journalist_articles,
        name="journalist_articles",
    ),
    path(
        "subscribe/<int:journalist_id>/",
        views.subscribe_journalist,
        name="subscribe_journalist",
    ),
    path(
        "article/<int:pk>/delete/", views.article_delete, name="article_delete"
    ),  # for editors
    path(
        "article/<int:pk>/delete_by_author/",
        views.article_delete_by_author,
        name="article_delete_by_author",
    ),
    path("category/<slug:slug>/", views.category_articles, name="category_articles"),
]
