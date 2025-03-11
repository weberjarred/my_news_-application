"""
Defines RESTful API views using Django REST Framework.
For example, the ArticleListAPI view returns articles filtered by
the reader’s subscriptions if the logged-in user is a reader.
"""

from rest_framework import generics, permissions
from .models import Article
from .serializers import ArticleSerializer
from django.db import models


class ArticleListCreateAPI(generics.ListCreateAPIView):
    queryset = Article.objects.all()  # or filter by role if needed
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "reader":
            publisher_ids = user.subscriptions_publishers.values_list(
                "id", flat=True
            )
            journalist_ids = user.subscriptions_journalists.values_list(
                "id", flat=True
            )
            return (
                Article.objects.filter(status="approved")
                .filter(
                    models.Q(publisher__id__in=publisher_ids)
                    | models.Q(author__id__in=journalist_ids)
                )
                .distinct()
            )
        return Article.objects.filter(status="approved")

    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)
