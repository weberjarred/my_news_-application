from .models import Category


def news_categories(request):
    return {"categories": Category.objects.all()}
