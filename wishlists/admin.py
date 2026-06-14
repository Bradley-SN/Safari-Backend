from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'updated_at')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('customer__email',)
    ordering = ('-updated_at',)
    inlines = [WishlistItemInline]


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('wishlist__customer__email', 'product__name')
    ordering = ('-added_at',)
