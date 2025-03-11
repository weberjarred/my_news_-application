# Generated by Django 5.1.7 on 2025-03-11 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsApp", "0002_article_is_deleted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="approved",
        ),
        migrations.AddField(
            model_name="article",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
