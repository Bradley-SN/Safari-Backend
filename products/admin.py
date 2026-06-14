from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'price', 'current_price', 'stock_quantity', 'availability_status', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'brand', 'availability_status', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [ProductImageInline]
    fieldsets = (
        ('Product Info', {'fields': ('name', 'slug', 'description', 'category', 'brand')}),
        ('Pricing & Stock', {'fields': ('sku', 'price', 'discount_price', 'stock_quantity')}),
        ('Attributes', {'fields': ('weight', 'color', 'size', 'delivery_estimate', 'tags')}),
        ('Status', {'fields': ('availability_status', 'is_featured', 'is_active')}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    ordering = ('-is_primary', '-created_at')
