from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'final_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer__email', 'shipping_city')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'customer', 'status')}),
        ('Pricing', {'fields': ('total_amount', 'tax_amount', 'delivery_fee', 'discount_amount', 'final_amount')}),
        ('Shipping Address', {'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_country', 'phone_number')}),
        ('Additional', {'fields': ('notes', 'created_at', 'updated_at')}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name')
    ordering = ('-created_at',)
