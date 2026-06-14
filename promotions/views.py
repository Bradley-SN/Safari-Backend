from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Coupon, PromotionalBanner, FlashSale
from .serializers import CouponSerializer, PromotionalBannerSerializer, FlashSaleSerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['code']
    filterset_fields = ['discount_type']


class PromotionalBannerViewSet(viewsets.ModelViewSet):
    queryset = PromotionalBanner.objects.filter(is_active=True).order_by('display_order')
    serializer_class = PromotionalBannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FlashSaleViewSet(viewsets.ModelViewSet):
    queryset = FlashSale.objects.filter(is_active=True)
    serializer_class = FlashSaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['title']
    filterset_fields = ['is_active']
