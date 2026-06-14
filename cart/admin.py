from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_items', 'total_price', 'updated_at')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('customer__email',)
    readonly_fields = ('total_items', 'total_price', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__customer__email', 'product__name')
    ordering = ('-added_at',)
