from django.urls import path
from carts import views
app_name = 'carts'
urlpatterns = [


    path('<slug:category_slug>/',views.catalog,name='index'),


    path('product/<slug:product_slug>',views.product,name='product'),


]