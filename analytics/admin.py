from django.contrib import admin
from .models import DailySalesReport, ProductAnalytics, CustomerAnalytics, StockAlerts


@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_orders', 'total_revenue', 'total_items_sold', 'average_order_value')
    list_filter = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)


@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'product_name', 'units_sold', 'revenue', 'views_count')
    list_filter = ('date',)
    search_fields = ('product_name',)
    ordering = ('-date', '-revenue')


@admin.register(CustomerAnalytics)
class CustomerAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_customers', 'new_customers', 'returning_customers', 'total_cart_abandonment')
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(StockAlerts)
class StockAlertsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'current_stock', 'reorder_level', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('product_name',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
