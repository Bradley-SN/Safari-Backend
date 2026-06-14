from rest_framework import serializers
from .models import Inventory, StockAdjustment


class StockAdjustmentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.first_name', read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = ['id', 'inventory', 'adjustment_type', 'quantity', 'reason', 
                  'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class InventorySerializer(serializers.ModelSerializer):
    adjustments = StockAdjustmentSerializer(many=True, read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    available_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'current_stock', 'reserved_stock', 
                  'reorder_level', 'available_stock', 'adjustments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_available_stock(self, obj):
        return obj.available_stock
