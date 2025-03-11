"""
App configuration for the newsApp app.

Configures the application and ensures that signal handlers are
loaded when the app is ready.
"""

from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsApp"

    def ready(self):
        # Import signals so that they are registered
        import newsApp.signals  # noqa: F401
