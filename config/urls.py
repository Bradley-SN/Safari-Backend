"""
URL configuration for Safari Stores E-Commerce Backend
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import all ViewSets
from authentication.views import UserViewSet
from categories.views import CategoryViewSet
from brands.views import BrandViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet
from payments.views import PaymentViewSet
from cart.views import CartViewSet
from reviews.views import ReviewViewSet
from wishlists.views import WishlistViewSet
from inventory.views import InventoryViewSet, StockAdjustmentViewSet
from shipment.views import ShipmentViewSet
from notifications.views import NotificationViewSet
from promotions.views import CouponViewSet, PromotionalBannerViewSet, FlashSaleViewSet
from analytics.views import DailySalesReportViewSet, ProductAnalyticsViewSet, CustomerAnalyticsViewSet, StockAlertsViewSet

# Create router and register viewsets
router = DefaultRouter()

# Authentication
router.register(r'users', UserViewSet, basename='user')

# Products & Categories
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')

# Orders & Payments
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'payments', PaymentViewSet, basename='payment')

# Shopping
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'wishlists', WishlistViewSet, basename='wishlist')

# Inventory & Shipment
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'stock-adjustments', StockAdjustmentViewSet, basename='stock-adjustment')
router.register(r'shipments', ShipmentViewSet, basename='shipment')

# Notifications & Promotions
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'banners', PromotionalBannerViewSet, basename='banner')
router.register(r'flash-sales', FlashSaleViewSet, basename='flash-sale')

# Analytics (Admin only)
router.register(r'analytics/sales', DailySalesReportViewSet, basename='sales-report')
router.register(r'analytics/products', ProductAnalyticsViewSet, basename='product-analytics')
router.register(r'analytics/customers', CustomerAnalyticsViewSet, basename='customer-analytics')
router.register(r'analytics/stock-alerts', StockAlertsViewSet, basename='stock-alerts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # DRF Auth (optional - for browsable API)
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
