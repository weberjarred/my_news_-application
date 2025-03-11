"""
This file contains unit tests which cover article creation,
approval, and API access using the Arrange-Act-Assert (AAA) pattern.

These tests ensure that journalists can create articles,
editors can approve them, and readers receive the correct API data.

Unit Testing: The tests implemented in the 'tests.py' file
utilize the Arrange-Act-Assert (AAA) pattern to thoroughly
verify the functionality associated with article creation,
approval processes, and the retrieval of data through the API.


new:
This file contains unit tests which cover article creation,
approval, and API access using the Arrange-Act-Assert (AAA) pattern.

These tests ensure that journalists can create articles,
editors can approve them, and readers receive the correct API data.

"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, Publisher
from rest_framework.test import APIClient

User = get_user_model()


class NewsAppTests(TestCase):
    def setUp(self):
        # ARRANGE: Create test users, publisher, and an article.
        self.client = Client()
        self.api_client = APIClient()
        self.reader = User.objects.create_user(
            username="reader1",
            password="Reader@123",
            role="reader",
            email="reader1@example.com",
        )
        self.journalist = User.objects.create_user(
            username="journalist1",
            password="Journalist@123",
            role="journalist",
            email="journalist1@example.com",
        )
        self.editor = User.objects.create_user(
            username="editor1",
            password="Editor@123",
            role="editor",
            email="editor1@example.com",
        )
        self.publisher = Publisher.objects.create(name="Test Publisher")
        # Add subscriptions so the reader follows this publisher and
        # journalist.
        self.reader.subscriptions_publishers.add(self.publisher)
        self.reader.subscriptions_journalists.add(self.journalist)
        self.article = Article.objects.create(
            title="Test Article",
            content="Content of test article.",
            author=self.journalist,
            publisher=self.publisher,
            status="pending",  # Using status instead of approved
        )

    def test_article_creation_by_journalist(self):
        # GIVEN a journalist is logged in.
        self.client.login(username="journalist1", password="Journalist@123")
        # WHEN the journalist submits an article.
        response = self.client.post(
            reverse("article_create"),
            {
                "title": "New Article",
                "content": "New article content",
                "publisher": self.publisher.id,
            },
        )
        # THEN the article is created and remains pending.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.get(title="New Article").status, "pending")

    def test_article_approval_by_editor(self):
        # GIVEN an editor is logged in.
        self.client.login(username="editor1", password="Editor@123")
        # WHEN the editor approves an article.
        response = self.client.post(
            reverse("article_approval"),
            {"article_id": self.article.id, "action": "approve"},
        )
        # THEN the article is approved.
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "approved")

    def test_api_article_list_for_reader(self):
        # Approve the test article.
        self.article.status = "approved"
        self.article.save()
        # GIVEN a reader is logged in via the API.
        self.api_client.login(username="reader1", password="Reader@123")
        # WHEN the reader fetches articles via the API.
        response = self.api_client.get(reverse("api_article_list"))
        # THEN the API response contains the approved article.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
