from django.contrib import admin
from .models import Inventory, StockAdjustment


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'current_stock', 'reserved_stock', 'available_stock', 'reorder_level', 'low_stock_alert', 'last_restocked_at')
    list_filter = ('updated_at', 'last_restocked_at')
    search_fields = ('product__name', 'product__sku')
    readonly_fields = ('available_stock', 'low_stock_alert')
    ordering = ('-updated_at',)


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'adjustment_type', 'reason', 'created_by', 'created_at')
    list_filter = ('adjustment_type', 'created_at')
    search_fields = ('product__name', 'reason', 'created_by')
    ordering = ('-created_at',)
