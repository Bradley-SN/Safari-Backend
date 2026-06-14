from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shipment, ShipmentTracking
from .serializers import ShipmentSerializer, ShipmentTrackingSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(order__customer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_shipments(self, request):
        shipments = self.get_queryset()
        serializer = self.get_serializer(shipments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_tracking(self, request, pk=None):
        shipment = self.get_object()
        status_update = request.data.get('status')
        location = request.data.get('location')
        message = request.data.get('message', '')
        
        shipment.status = status_update
        shipment.save()
        
        ShipmentTracking.objects.create(
            shipment=shipment,
            status=status_update,
            location=location,
            message=message
        )
        
        return Response(ShipmentSerializer(shipment).data)
