from django.contrib import admin

# Register your models here.
from goods.models import Categories,Products
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):

    list_display = ['name','price','quantity']
    list_editable = ['price','quantity']
    search_fields = ['name','description']
    list_filter = ['category','quantity']
    fields=[
        'name',
        'category',
        'description',
        'image',
        'price',
        'quantity',
    ]

