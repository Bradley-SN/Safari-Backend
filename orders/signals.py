"""
Django signals for Orders app
Handles email notifications when orders are created
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from core_services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """
    Send order confirmation email when order is created
    
    Args:
        sender: Model class
        instance: Order instance
        created: Boolean indicating if the instance was created
        **kwargs: Additional keyword arguments
    """
    if created:
        try:
            # Get customer
            customer = instance.customer
            
            # Send confirmation email
            EmailService.send_order_confirmation(
                order=instance,
                customer=customer,
                admin_emails=['admin@safaristores.com']
            )
            
            logger.info(f"Order confirmation email sent for order {instance.order_number}")
            
        except Exception as e:
            logger.error(f"Error sending order confirmation email: {str(e)}")
