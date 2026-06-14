from django.contrib import admin
from .models import Shipment, ShipmentTracking


class ShipmentTrackingInline(admin.TabularInline):
    model = ShipmentTracking
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'order', 'status', 'estimated_delivery_date', 'actual_delivery_date', 'courier_name', 'updated_at')
    list_filter = ('status', 'estimated_delivery_date', 'created_at')
    search_fields = ('tracking_number', 'order__order_number', 'courier_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [ShipmentTrackingInline]
    fieldsets = (
        ('Shipment Info', {'fields': ('order', 'tracking_number', 'status')}),
        ('Delivery Details', {'fields': ('delivery_location', 'delivery_fee', 'estimated_delivery_date', 'actual_delivery_date')}),
        ('Courier Info', {'fields': ('courier_name', 'rider_name', 'rider_phone', 'vehicle_info')}),
        ('Additional', {'fields': ('notes', 'created_at', 'updated_at')}),
    )


@admin.register(ShipmentTracking)
class ShipmentTrackingAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'status', 'location', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shipment__tracking_number', 'location', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
