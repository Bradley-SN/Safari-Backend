from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']
        read_only_fields = ['id']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category_name', 'brand_name', 'sku',
            'price', 'discount_price', 'current_price', 'discount_percentage',
            'images',
            'stock_quantity', 'availability_status', 'is_featured', 'created_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']