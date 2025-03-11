"""
Defines the core data models for CustomUser, Publisher, Article,
and the Newsletter.

The CustomUser model extends Django’s AbstractUser and includes
a role field as well as subscriptions for readers.

The Article model has an “approved” flag, and the Publisher model
relates to multiple editors and journalists.

The custom user model and group assignments in models.py
guarantee user role assignments. The views limit access according
to these roles (for instance, only journalists are allowed to
create articles, while only editors can approve them).

Additionally, the registration form enforces password
complexity requirements.

This file includes a secure article removal feature for editors,
utilizing a soft-delete mechanism. Instead of permanently removing
an article from the database, you can simply mark it as removed
(or archived). This approach not only ensures an audit trail but
also allows for the recovery of the article if necessary.

"""

from django.db import models
from django.contrib.auth.models import AbstractUser


# Define available roles
ROLE_CHOICES = (
    ("reader", "Reader"),
    ("editor", "Editor"),
    ("journalist", "Journalist"),
)

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
]


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    subscriptions_publishers = models.ManyToManyField(
        "Publisher", blank=True, related_name="subscribed_readers"
    )
    subscriptions_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="subscribed_readers_by"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically add user to a group based on their role.
        from django.contrib.auth.models import Group

        group, created = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)

    def __str__(self):
        return self.username


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # A publisher can have multiple editors and journalists.
    editors = models.ManyToManyField(
        CustomUser, blank=True, related_name="editing_publishers"
    )
    journalists = models.ManyToManyField(
        CustomUser, blank=True, related_name="journalism_publishers"
    )

    def __str__(self):
        return self.name


# soft-delete functionality employed
# clearer distinction between “Pending,” “Approved,” and “Rejected,” added.
# A status field is added to the Article model.
class Article(models.Model):
    CATEGORY_CHOICES = [
        ("news", "News"),
        ("business", "Business"),
        ("tech", "Tech"),
        ("sport", "Sport"),
        ("investigations", "Investigations"),
        ("politics", "Politics"),
        ("opinion", "Opinion"),
        ("life", "Life"),
        ("food", "Food"),
        ("climate", "Climate/Future"),
        ("projects", "Special Projects"),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    # Instead of just approved=True/False, we track multiple states:
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
    )

    def __str__(self):
        return self.title

    # helper methods:
    def approve(self, editor):
        """Set status to 'approved' and record the editor who approved it."""
        self.status = "approved"
        self.approved_by = editor
        self.save()

    def reject(self):
        """Set status to 'rejected'."""
        self.status = "rejected"
        self.save()

    def is_approved(self):
        """Check if article is in 'approved' status."""
        return self.status == "approved"


# Create a Category Model
class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    journalist = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="newsletters"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters",
    )
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
