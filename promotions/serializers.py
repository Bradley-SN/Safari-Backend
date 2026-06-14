from rest_framework import serializers
from .models import Coupon, PromotionalBanner, FlashSale
from products.serializers import ProductListSerializer


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'max_discount', 
                  'min_purchase_amount', 'usage_limit', 'usage_count', 'start_date', 
                  'end_date', 'is_valid', 'created_at']
        read_only_fields = ['id', 'usage_count', 'created_at']

    def get_is_valid(self, obj):
        return obj.is_valid


class PromotionalBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalBanner
        fields = ['id', 'title', 'description', 'image', 'link', 'is_active', 
                  'start_date', 'end_date', 'display_order', 'created_at']
        read_only_fields = ['id', 'created_at']


class FlashSaleSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    
    class Meta:
        model = FlashSale
        fields = ['id', 'title', 'description', 'discount_percentage', 'start_date', 
                  'end_date', 'is_active', 'products', 'created_at']
        read_only_fields = ['id', 'created_at']