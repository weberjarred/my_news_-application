"""
Contains the view functions for user registration, login,
logout, dashboard, article creation (for journalists), article
approval (for editors), article listing, and article detail pages.

Access control is enforced via decorators.
(Note: The email sending and posting to X are handled via Django signals.)

This section introduces a view enabling an editor to "remove"
an article. In this instance, the view shows a confirmation page
(through a GET request), and subsequently marks the article as deleted
when the editor confirms (using a POST request).

"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ArticleForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Article, CustomUser, Category

# from django.core.mail import send_mail
# from django.conf import settings
from django.http import HttpResponseForbidden


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "newsApp/register.html", {"form": form})


def user_login(request):
    from django.contrib.auth.forms import AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "newsApp/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    context = {}
    if request.user.role == "journalist":
        # Show all articles authored by the journalist
        user_articles = Article.objects.filter(
            author=request.user, is_deleted=False
        ).order_by("-created_at")
        context["user_articles"] = user_articles

    elif request.user.role == "editor":
        # Show only articles that are pending
        pending_articles = Article.objects.filter(
            status="pending", is_deleted=False
        ).order_by("-created_at")
        context["pending_articles"] = pending_articles

    return render(request, "newsApp/dashboard.html", context)


@login_required
def article_create(request):
    # Only journalists are allowed to create articles.
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
        return redirect("dashboard")
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article submitted for approval.")
            return redirect("dashboard")
        else:
            # Log or print form errors for debugging
            print(form.errors)
            messages.error(request, "There were errors in your submission.")
    else:
        form = ArticleForm()
    return render(request, "newsApp/article_form.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.role == "editor")
def article_approval(request):
    pending_articles = Article.objects.filter(status="pending", is_deleted=False)

    if request.method == "POST":
        article_id = request.POST.get("article_id")
        action = request.POST.get("action")  # "approve" or "reject"
        article = get_object_or_404(
            Article, id=article_id, status="pending", is_deleted=False
        )

        if action == "approve":
            article.approve(request.user)  # sets status='approved'
            messages.success(request, "Article approved.")
            # Signals can handle notifications to subscribers.

        elif action == "reject":
            article.reject()  # sets status='rejected'
            messages.warning(request, "Article rejected.")
            # Optionally email the author about rejection.

        return redirect("dashboard")  # or redirect('article_approval')

    return render(
        request, "newsApp/article_approval.html", {"pending_articles": pending_articles}
    )


def article_list(request):
    articles = Article.objects.filter(status="approved", is_deleted=False).order_by(
        "-created_at"
    )
    return render(request, "newsApp/article_list.html", {"articles": articles})


@login_required
def article_detail(request, pk):
    if request.user.role == "editor":
        # Editors can view any article that isn’t soft-deleted.
        article = get_object_or_404(Article, pk=pk, is_deleted=False)
    elif request.user.role == "journalist":
        # Journalists can view their own articles regardless of status.
        article = get_object_or_404(Article, pk=pk, is_deleted=False)
        if article.author != request.user and article.status != "approved":
            # Prevent journalists from viewing others' unapproved articles.
            return HttpResponseForbidden("You are not allowed to view this article.")
    else:
        # Readers see only approved articles.
        article = get_object_or_404(Article, pk=pk, status="approved", is_deleted=False)

    return render(request, "newsApp/article_detail.html", {"article": article})


@login_required
@user_passes_test(lambda u: u.role == "editor")
def article_delete(request, pk):
    # Only consider articles that are approved and not already removed
    article = get_object_or_404(Article, pk=pk, approved=True, is_deleted=False)

    if request.method == "POST":
        # Soft-delete the article
        article.is_deleted = True
        article.save()
        messages.success(request, "Article has been removed.")
        return redirect("article_list")

    # Render a confirmation page
    return render(request, "newsApp/article_confirm_delete.html", {"article": article})


# Create the Subscription View
@login_required
def subscribe_journalist(request, journalist_id):
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to journalists.")
        return redirect("dashboard")

    journalist = get_object_or_404(CustomUser, pk=journalist_id, role="journalist")
    request.user.subscriptions_journalists.add(journalist)
    messages.success(request, f"You have subscribed to {journalist.username}.")
    return redirect("subscriptions")  # or anywhere you prefer


# Create a “Subscriptions” Page
@login_required
def subscriptions(request):
    # Ensure only readers see subscriptions
    if request.user.role != "reader":
        messages.error(request, "Only readers have subscriptions.")
        return redirect("dashboard")

    # Retrieve all journalists the reader is subscribed to
    subscribed_journalists = request.user.subscriptions_journalists.all()
    return render(
        request,
        "newsApp/subscriptions.html",
        {"subscribed_journalists": subscribed_journalists},
    )


@login_required
def journalist_articles(request, journalist_id):
    # Get the journalist by id and ensure their role is 'journalist'
    journalist = get_object_or_404(CustomUser, id=journalist_id, role="journalist")
    # Retrieve only approved, non-deleted articles by this journalist
    articles = Article.objects.filter(
        author=journalist, status="approved", is_deleted=False
    ).order_by("-created_at")

    return render(
        request,
        "newsApp/journalist_articles.html",
        {"journalist": journalist, "articles": articles},
    )


# separate view that allows a journalist to delete (soft-delete) an
# article if it’s rejected
@login_required
def article_delete_by_author(request, pk):
    # Only allow deletion if the article is not already deleted,
    # is authored by the logged-in journalist, and is rejected.
    article = get_object_or_404(
        Article, pk=pk, is_deleted=False, author=request.user, status="rejected"
    )

    if request.method == "POST":
        article.is_deleted = True
        article.save()
        messages.success(request, "Article deleted successfully.")
        return redirect("dashboard")

    return render(request, "newsApp/article_confirm_delete.html", {"article": article})


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Filter articles that belong to this category (and perhaps are approved,
    # not deleted, etc.)
    articles = Article.objects.filter(
        category=category, status="approved", is_deleted=False
    )
    return render(
        request,
        "newsApp/category_articles.html",
        {
            "category": category,
            "articles": articles,
        },
    )


@login_required
def homepage(request):
    # Get all approved, non-deleted articles ordered by newest first
    articles = Article.objects.filter(status="approved", is_deleted=False).order_by(
        "-created_at"
    )
    return render(request, "newsApp/homepage.html", {"articles": articles})
