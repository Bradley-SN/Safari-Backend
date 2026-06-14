from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
import uuid


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['order_number']
    ordering_fields = ['created_at', 'final_amount']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        cart = request.user.cart
        items = cart.items.all()
        
        if not items.exists():
            return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = cart.total_price
        order = Order.objects.create(
            order_number=order_number,
            customer=request.user,
            total_amount=total_amount,
            final_amount=total_amount,
            **serializer.validated_data
        )
        
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.current_price,
                subtotal=item.subtotal
            )
        
        cart.items.all().delete()
        
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        return Response(OrderDetailSerializer(order).data)
