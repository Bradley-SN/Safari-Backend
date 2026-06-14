from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'is_verified_purchase', 'is_approved', 'helpful_count', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('product__name', 'customer__email', 'title', 'comment')
    readonly_fields = ('helpful_count', 'unhelpful_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
