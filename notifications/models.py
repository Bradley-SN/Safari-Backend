from django.db import models
from authentication.models import User
from orders.models import Order


class Notification(models.Model):
    """Notification Model"""
    NOTIFICATION_TYPE_CHOICES = [
        ('order_confirmation', 'Order Confirmation'),
        ('order_status', 'Order Status Update'),
        ('delivery_update', 'Delivery Update'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('low_stock', 'Low Stock Alert'),
        ('promotional', 'Promotional'),
        ('system', 'System'),
    ]
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-App'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['is_sent']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} to {self.recipient.email}"
