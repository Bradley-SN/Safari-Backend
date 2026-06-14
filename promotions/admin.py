from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Coupon, PromotionalBanner, FlashSale


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'discount_type', 'discount_value', 'usage_count',
        'usage_limit', 'validity_status', 'is_active', 'start_date', 'end_date'
    )
    list_filter = ('discount_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('code', 'description')
    # is_valid is a property — it can't be in readonly_fields directly
    readonly_fields = ('usage_count', 'created_at', 'updated_at', 'validity_status')
    ordering = ('-created_at',)
    fieldsets = (
        ('Coupon Details', {
            'fields': ('code', 'description', 'discount_type', 'discount_value', 'max_discount')
        }),
        ('Usage & Limits', {
            'fields': ('min_purchase_amount', 'usage_limit', 'usage_count')
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date', 'is_active', 'validity_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Valid Now?', boolean=True)
    def validity_status(self, obj):
        return obj.is_valid


@admin.register(PromotionalBanner)
class PromotionalBannerAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_order', 'start_date', 'end_date',
        'is_active', 'banner_preview', 'created_at'
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('display_order', '-created_at')
    readonly_fields = ('created_at', 'banner_preview')
    fieldsets = (
        ('Banner Details', {
            'fields': ('title', 'description', 'image', 'banner_preview', 'link')
        }),
        ('Scheduling', {
            'fields': ('start_date', 'end_date', 'is_active', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Preview')
    def banner_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 120px; '
                'object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '—'


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'discount_percentage', 'start_date',
        'end_date', 'is_active', 'product_count'
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('products',)
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'product_count')
    fieldsets = (
        ('Sale Details', {
            'fields': ('title', 'description', 'discount_percentage')
        }),
        ('Scheduling', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Products', {
            'fields': ('products', 'product_count')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='# Products')
    def product_count(self, obj):
        return obj.products.count()