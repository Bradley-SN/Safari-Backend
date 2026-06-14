from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_wishlist(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(customer=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(customer=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = __import__('products.models', fromlist=['Product']).Product.objects.get(id=product_id)
        except:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')
        wishlist = request.user.wishlist
        
        try:
            item = WishlistItem.objects.get(wishlist=wishlist, product_id=product_id)
            item.delete()
        except WishlistItem.DoesNotExist:
            return Response({'detail': 'Item not in wishlist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
