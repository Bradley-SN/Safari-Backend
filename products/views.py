from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImage
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'brand', 'availability_status', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        from inventory.models import Inventory
        low_stock = Product.objects.filter(
            is_active=True,
            inventory__low_stock_alert=True
        ).select_related('category', 'brand')
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def upload_image(self, request, pk=None):
        product = self.get_object()
        image = request.FILES.get('image')
        if not image:
            return Response({'detail': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_primary = request.data.get('is_primary', False)
        if is_primary:
            ProductImage.objects.filter(product=product, is_primary=True).update(is_primary=False)
        
        prod_image = ProductImage.objects.create(product=product, image=image, is_primary=is_primary)
        return Response({'detail': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
