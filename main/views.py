from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories
def index(request):
    categories = Categories.objects.all()
    context = {
        'title':'Home',
        'content':'Main page of the coffe shop - HOME',



    }
    return render(request,'main/index.html',context)
def about(request):
    context = {
        'title': 'About us',
        'content': 'About us',
        'text_on_page': """Welcome to our coffee shop – a place where every cup is brewed with passion and care.
We believe that coffee is more than just a drink; it is a moment of comfort, inspiration, and connection.

Our baristas carefully select high‑quality beans from around the world and roast them to bring out their unique aroma and taste. Whether you enjoy a strong espresso, a smooth latte, or a perfectly balanced cappuccino, we prepare every drink as if it were for a friend.

Beyond coffee, we offer a cozy atmosphere – a warm space to meet with friends, work on new ideas, or simply take a break from your day.

Thank you for being a part of our story. Sit back, relax, and enjoy your cup of happiness with us."""
    }
    return render(request, 'main/about.html', context)