"""
This file is used to creates serializers which converts Django model
instances into JSON files for API interaction.
"""

from rest_framework import serializers
from .models import Article, Newsletter, Publisher


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "publisher",
            "status",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
