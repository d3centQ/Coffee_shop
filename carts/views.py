from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from carts.models import Cart
from goods.models import Products
from carts.utils import get_user_carts
from django.template.loader import render_to_string


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
    else:
        carts=Cart.objects.filter(
            session_key=request.session.session_key,product=product)
        if carts.exists():
            cart=carts.first()
            if cart:
                cart.quantity = cart.quantity + 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key ,product=product,quantity=1)













    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='user:login')
def cart_change(request, cart_id):
    action = request.GET.get("action")
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    if action == "inc":
        cart.quantity += 1
        cart.save()
    elif action == "dec":
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()

    return redirect(request.META.get("HTTP_REFERER", "main:index"))

def cart_remove(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    Cart.objects.filter(user=request.user, product=product).delete()

    return redirect(request.META.get('HTTP_REFERER', 'main:index'))