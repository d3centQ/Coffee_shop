from django.shortcuts import render, get_object_or_404

from carts.models import Cart
from goods.models import Products
from django.shortcuts import redirect


# Create your views here.
def cart_add(request,product_slug):
    product =Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user,product=product)
        if carts.exists():
            cart=carts.first()
            if cart:
                cart.quantity = cart.quantity + 1
                cart.save()
        else:
            Cart.objects.create(user=request.user,product=product,quantity=1)
    return redirect(request.META['HTTP_REFERER'])

def cart_change(request,product_slug):
    ...

def cart_remove(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    Cart.objects.filter(user=request.user, product=product).delete()

    return redirect(request.META.get('HTTP_REFERER', 'main:index'))