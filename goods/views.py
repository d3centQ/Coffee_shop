from django.core.paginator import Paginator
from django.shortcuts import render
from goods.models import Products, Categories
from goods.utils import q_search
from django.http import Http404


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale')
    order_by = request.GET.get('order_by')
    query = (request.GET.get('query') or '').strip()

    # SEARCH has priority
    if query:
        goods = q_search(query) or Products.objects.none()
        selected_category = None
    elif category_slug == "all-stock" or category_slug is None:
        goods = Products.objects.all()
        selected_category = Categories.objects.filter(slug="all-stock").first()
    else:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404()
        selected_category = Categories.objects.filter(slug=category_slug).first()

    # Filters
    if on_sale == 'on':
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    current_page = Paginator(goods, 6).get_page(page)
    all_categories = Categories.objects.all()

    context = {
        "title": "Home - Catalog",
        "goods": current_page,
        "slug_url": category_slug,
        "selected_category": selected_category,
        "categories": all_categories,
        "q": query,  # pass search query to template
    }

    return render(request, "goods/catalog.html", context)


def search(request):
    page = request.GET.get('page', 1)
    q = (request.GET.get('query') or request.GET.get('q') or '').strip()
    goods = q_search(q)
    current_page = Paginator(goods, 3).get_page(page)
    ctx = {"title": "Search", "goods": current_page, "q": q, "slug_url": None}
    return render(request, "goods/catalog.html", ctx)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {"product": product}
    return render(request, "goods/product.html", context)
