from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, PaymentLog
from .serializers import PaymentSerializer
from core_services.daraja_service import get_daraja_client
from core_services.email_service import EmailService
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__customer=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def initiate_mpesa(self, request):
        """
        Initiate M-Pesa STK Push payment for an order
        
        Request body:
        {
            "order_id": 1,
            "phone_number": "254712345678"  # Format: 254XXXXXXXXX
        }
        """
        try:
            order_id = request.data.get('order_id')
            phone_number = request.data.get('phone_number')
            
            if not order_id or not phone_number:
                return Response(
                    {'error': 'order_id and phone_number are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate phone number format
            if not phone_number.startswith('254'):
                return Response(
                    {'error': 'Phone number must be in format 254XXXXXXXXX'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create payment
            try:
                from orders.models import Order
                order = Order.objects.get(id=order_id, customer=request.user)
            except Order.DoesNotExist:
                return Response(
                    {'error': 'Order not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if payment already exists
            if hasattr(order, 'payment'):
                if order.payment.status == 'paid':
                    return Response(
                        {'error': 'Order already paid'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                payment = order.payment
            else:
                # Create new payment
                payment = Payment.objects.create(
                    order=order,
                    amount=order.final_amount,
                    payment_method='mpesa',
                    phone_number=phone_number
                )
            
            # Initiate STK Push via Daraja API
            daraja = get_daraja_client()
            
            result = daraja.stk_push(
                phone_number=phone_number,
                amount=int(payment.amount),
                account_reference=order.order_number,
                description=f'Payment for order {order.order_number}',
                callback_url='http://127.0.0.1:8000/api/payments/mpesa-callback/'  # Will be overridden with settings
            )
            
            if result.get('success'):
                # Store checkout request ID
                payment.checkout_request_id = result.get('checkout_request_id')
                payment.save()
                
                # Log the transaction
                PaymentLog.objects.create(
                    payment=payment,
                    status='pending',
                    message=f'STK Push initiated: {result.get("customer_message")}',
                    response_code=result.get('response_code')
                )
                
                return Response({
                    'success': True,
                    'message': result.get('customer_message'),
                    'checkout_request_id': result.get('checkout_request_id'),
                    'payment_id': payment.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': result.get('error'),
                    'response_code': result.get('response_code')
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error initiating M-Pesa payment: {str(e)}")
            return Response(
                {'error': f'Error initiating payment: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def query_mpesa_status(self, request):
        """
        Query M-Pesa payment status
        
        Request body:
        {
            "checkout_request_id": "ws_CO_28062226234656878"
        }
        """
        try:
            checkout_request_id = request.data.get('checkout_request_id')
            
            if not checkout_request_id:
                return Response(
                    {'error': 'checkout_request_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get payment
            try:
                payment = Payment.objects.get(
                    checkout_request_id=checkout_request_id,
                    order__customer=request.user
                )
            except Payment.DoesNotExist:
                return Response(
                    {'error': 'Payment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Query status via Daraja
            daraja = get_daraja_client()
            result = daraja.query_transaction_status(checkout_request_id)
            
            if result.get('success') and result.get('status') == 'completed':
                # Update payment as paid
                payment.status = 'paid'
                payment.transaction_id = result.get('mpesa_receipt_number')
                payment.mpesa_receipt_number = result.get('mpesa_receipt_number')
                payment.save()
                
                # Update order status
                payment.order.status = 'confirmed'
                payment.order.save()
                
                # Log the transaction
                PaymentLog.objects.create(
                    payment=payment,
                    status='paid',
                    message=f'Payment confirmed: {result.get("result_desc")}',
                    response_code=result.get('response_code')
                )
                
                # Send payment confirmation email
                EmailService.send_payment_confirmation(
                    payment=payment,
                    order=payment.order,
                    customer=payment.order.customer
                )
                
                return Response({
                    'success': True,
                    'status': 'paid',
                    'message': 'Payment confirmed',
                    'receipt_number': result.get('mpesa_receipt_number')
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'status': result.get('status', 'pending'),
                    'message': result.get('error', 'Payment still pending')
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error querying M-Pesa status: {str(e)}")
            return Response(
                {'error': f'Error querying status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_paid(self, request, pk=None):
        payment = self.get_object()
        if payment.status == 'pending':
            payment.status = 'paid'
            payment.save()
            
            payment.order.status = 'confirmed'
            payment.order.save()
            
            PaymentLog.objects.create(
                payment=payment,
                status='paid',
                message='Payment marked as paid by admin'
            )
            
            # Send confirmation email
            EmailService.send_payment_confirmation(
                payment=payment,
                order=payment.order,
                customer=payment.order.customer
            )
            
            return Response(PaymentSerializer(payment).data)
        return Response({'detail': 'Payment already processed'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_failed(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'failed'
        payment.save()
        
        PaymentLog.objects.create(
            payment=payment,
            status='failed',
            message=request.data.get('reason', 'Payment failed')
        )
        return Response(PaymentSerializer(payment).data)

