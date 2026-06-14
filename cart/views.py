from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _get_serializer_context(self, request):
        """Pass request into serializer so image URLs are absolute."""
        return {'request': request}

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        serializer = CartSerializer(cart, context=self._get_serializer_context(request))
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            from products.models import Product
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': int(quantity)}
        )

        if not created:
            item.quantity += int(quantity)
            item.save()

        serializer = CartSerializer(cart, context=self._get_serializer_context(request))
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')

        # Use get_or_create so this never crashes on a missing cart
        cart, _ = Cart.objects.get_or_create(customer=request.user)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {'detail': 'Item not in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(cart, context=self._get_serializer_context(request))
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        # Use get_or_create so this never crashes on a missing cart
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart.items.all().delete()

        serializer = CartSerializer(cart, context=self._get_serializer_context(request))
        return Response(serializer.data)