from django.contrib import admin
from .models import Product, Store, Productparams

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city', 'country']

    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'weight', 'length', 'width', 'height']
    
    search_fields = ['name']


@admin.register(Productparams)
class ProductparamsAdmin(admin.ModelAdmin):
    list_display = ['productid', 'key', 'value', ]

    search_fields = ['key', 'value']