from rest_framework import serializers
from .models import Shipment, ShipmentTracking


class ShipmentTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentTracking
        fields = ['id', 'status', 'location', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class ShipmentSerializer(serializers.ModelSerializer):
    tracking_updates = ShipmentTrackingSerializer(many=True, read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = Shipment
        fields = ['id', 'order', 'order_number', 'tracking_number', 'status', 
                  'courier', 'estimated_delivery_date', 'actual_delivery_date', 
                  'rider_name', 'rider_phone', 'tracking_updates', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
