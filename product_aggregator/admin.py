# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Token, Product, Offer


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'author',
        'name',
        'description',
        'registered',
    )
    list_filter = ('created', 'registered')
    search_fields = ('name',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'author',
        'price',
        'items_in_stock',
        'product',
    )
    list_filter = ('created', 'product')
