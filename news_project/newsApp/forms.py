"""
This file contains Contains forms for user
registration and article submission. The custom registration
form enforces password complexity (including uppercase,
lowercase, digit, and special character rules).
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Article, Category
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check that both passwords were provided
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")

            # Validate password complexity on password2
            # (or password1, as they are the same)
            if not re.search(r"[A-Z]", password2):
                raise forms.ValidationError(
                    "Password must contain at least one uppercase letter."
                )
            if not re.search(r"[a-z]", password2):
                raise forms.ValidationError(
                    "Password must contain at least one lowercase letter."
                )
            if not re.search(r"\d", password2):
                raise forms.ValidationError(
                    "Password must contain at least one digit."
                )
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password2):
                raise forms.ValidationError(
                    "Password must contain at least one special character."
                )
        return cleaned_data


class LoginForm(AuthenticationForm):
    pass


# Removed duplicate ArticleForm definition


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,  # Set to True if you want to enforce selection
        empty_label="Select a category",
    )

    class Meta:
        model = Article
        fields = ["title", "content", "publisher", "category"]
