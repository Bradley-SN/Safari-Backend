from django.db import models
from orders.models import Order
from django.core.validators import MinValueValidator


class Shipment(models.Model):
    """Shipment/Delivery Model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed Delivery'),
        ('returned', 'Returned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_location = models.TextField()
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_date = models.DateField(blank=True, null=True)
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    rider_name = models.CharField(max_length=100, blank=True, null=True)
    rider_phone = models.CharField(max_length=20, blank=True, null=True)
    vehicle_info = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Shipment for {self.order.order_number}"


class ShipmentTracking(models.Model):
    """Track shipment status updates"""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_updates')
    status = models.CharField(max_length=30)
    location = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.status} for {self.shipment.tracking_number}"
