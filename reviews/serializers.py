from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'customer', 'customer_name', 
                  'rating', 'comment', 'is_verified_purchase', 'is_approved', 
                  'helpful_count', 'unhelpful_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'helpful_count', 'unhelpful_count', 'created_at', 'updated_at']
