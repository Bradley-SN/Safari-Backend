from rest_framework import serializers
from .models import DailySalesReport, ProductAnalytics, CustomerAnalytics, StockAlerts


class DailySalesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySalesReport
        fields = ['id', 'date', 'total_orders', 'total_revenue', 'total_items_sold', 
                  'average_order_value', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductAnalyticsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductAnalytics
        fields = ['id', 'product', 'product_name', 'date', 'units_sold', 'revenue', 
                  'views', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomerAnalyticsSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    
    class Meta:
        model = CustomerAnalytics
        fields = ['id', 'customer', 'customer_email', 'date', 'total_spent', 'orders_count', 
                  'average_order_value', 'created_at']
        read_only_fields = ['id', 'created_at']


class StockAlertsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = StockAlerts
        fields = ['id', 'product', 'product_name', 'current_stock', 'reorder_level', 
                  'is_resolved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
