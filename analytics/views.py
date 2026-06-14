from rest_framework import viewsets, permissions
from .models import DailySalesReport, ProductAnalytics, CustomerAnalytics, StockAlerts
from .serializers import DailySalesReportSerializer, ProductAnalyticsSerializer, CustomerAnalyticsSerializer, StockAlertsSerializer


class DailySalesReportViewSet(viewsets.ModelViewSet):
    queryset = DailySalesReport.objects.all().order_by('-date')
    serializer_class = DailySalesReportSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['date']
    ordering_fields = ['date', 'total_revenue']


class ProductAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = ProductAnalytics.objects.all().order_by('-date')
    serializer_class = ProductAnalyticsSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['date', 'product_id']
    search_fields = ['product_name']
    ordering_fields = ['date', 'revenue', 'units_sold']


class CustomerAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = CustomerAnalytics.objects.all().order_by('-date')
    serializer_class = CustomerAnalyticsSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['date']
    ordering_fields = ['date']


class StockAlertsViewSet(viewsets.ModelViewSet):
    queryset = StockAlerts.objects.filter(is_resolved=False).order_by('-created_at')
    serializer_class = StockAlertsSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['is_resolved']
    search_fields = ['product_name']
