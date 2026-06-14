from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Inventory, StockAdjustment
from .serializers import InventorySerializer, StockAdjustmentSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['product']
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_items = Inventory.objects.filter(low_stock_alert=True)
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        inventory = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        adjustment_type = request.data.get('adjustment_type', 'decrease')
        reason = request.data.get('reason', '')
        
        if adjustment_type == 'increase':
            inventory.current_stock += quantity
        else:
            inventory.current_stock = max(0, inventory.current_stock - quantity)
        
        inventory.save()
        
        StockAdjustment.objects.create(
            product=inventory.product,
            quantity=quantity,
            adjustment_type=adjustment_type,
            reason=reason,
            created_by=request.user.email
        )
        
        return Response(InventorySerializer(inventory).data)


class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['adjustment_type', 'product']
    ordering_fields = ['created_at']
