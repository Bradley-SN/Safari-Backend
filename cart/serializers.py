from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.current_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    # Alias so frontend can use either item.price or item.product_price
    price = serializers.DecimalField(
        source='product.current_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    # Explicit product_id field so frontend doesn't have to use item.product (the FK int)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    # Primary image URL from the product's images relation
    image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',       # FK int (kept for backwards compat)
            'product_id',    # explicit int alias
            'product_name',
            'product_price',
            'price',         # alias for frontend
            'image',
            'quantity',
            'subtotal',
        ]
        read_only_fields = ['id', 'subtotal']

    def get_image(self, obj):
        """
        Returns the absolute URL of the product's primary image.
        Falls back to the first image if no primary is set.
        """
        images = obj.product.images.all()
        primary = images.filter(is_primary=True).first() or images.first()
        if not primary:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(primary.image.url)
        return primary.image.url


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'customer',
            'items',
            'total_items',
            'total_price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'customer', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return obj.total_price

    def get_total_items(self, obj):
        return obj.total_items