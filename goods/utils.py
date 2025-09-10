from django.db.models import Q
from .models import Products

def q_search(query: str):
    if not query:
        return Products.objects.none()
    return Products.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(slug__icontains=query) |
        Q(category__name__icontains=query) |
        Q(category__slug__icontains=query)
    ).distinct()
