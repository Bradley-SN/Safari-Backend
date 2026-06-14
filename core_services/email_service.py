"""
Email Service Module
Handles sending emails for order confirmations and notifications
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_order_confirmation(order, customer, admin_emails=None):
        """
        Send order confirmation email to customer and admins
        
        Args:
            order: Order instance
            customer: User instance (customer)
            admin_emails: List of admin email addresses
        """
        try:
            # Default admin emails if not provided
            if not admin_emails:
                admin_emails = ['admin@safaristores.com']
            
            # Prepare context
            context = {
                'order': order,
                'customer': customer,
                'site_name': 'Safari Stores',
                'order_items': order.items.all(),
            }
            
            # Render email templates
            subject = f'Order Confirmation - {order.order_number}'
            
            # HTML version
            html_content = render_to_string('order_confirmation.html', context)
            
            # Text version
            text_content = render_to_string('order_confirmation.txt', context)
            
            # Send to customer
            if customer.email:
                _send_email(
                    subject=subject,
                    text_content=text_content,
                    html_content=html_content,
                    recipient_list=[customer.email]
                )
                logger.info(f"Order confirmation email sent to customer: {customer.email}")
            
            # Send to admins
            admin_subject = f'[ADMIN] New Order Received - {order.order_number}'
            admin_context = context.copy()
            admin_context['is_admin'] = True
            
            admin_html = render_to_string('order_confirmation.html', admin_context)
            admin_text = render_to_string('order_confirmation.txt', admin_context)
            
            _send_email(
                subject=admin_subject,
                text_content=admin_text,
                html_content=admin_html,
                recipient_list=admin_emails
            )
            logger.info(f"Order notification email sent to admins: {', '.join(admin_emails)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending order confirmation email: {str(e)}")
            return False
    
    @staticmethod
    def send_payment_confirmation(payment, order, customer, admin_emails=None):
        """
        Send payment confirmation email
        
        Args:
            payment: Payment instance
            order: Order instance
            customer: User instance
            admin_emails: List of admin email addresses
        """
        try:
            if not admin_emails:
                admin_emails = ['admin@safaristores.com']
            
            subject = f'Payment Confirmation - {order.order_number}'
            
            context = {
                'order': order,
                'customer': customer,
                'payment': payment,
                'site_name': 'Safari Stores',
            }
            
            message = f"""
            Payment Confirmed
            
            Order Number: {order.order_number}
            Transaction ID: {payment.transaction_id}
            Amount: KES {payment.amount}
            Payment Method: {payment.get_payment_method_display()}
            
            Thank you for your payment!
            """
            
            _send_email(
                subject=subject,
                text_content=message,
                recipient_list=[customer.email] if customer.email else []
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending payment confirmation email: {str(e)}")
            return False
    
    @staticmethod
    def send_shipment_notification(shipment, order, customer):
        """
        Send shipment notification email
        
        Args:
            shipment: Shipment instance
            order: Order instance
            customer: User instance
        """
        try:
            subject = f'Your Order is on the Way - {order.order_number}'
            
            message = f"""
            Your order is on the way!
            
            Order Number: {order.order_number}
            Tracking Number: {shipment.tracking_number}
            Courier: {shipment.courier}
            Estimated Delivery: {shipment.estimated_delivery_date}
            
            Track your shipment: http://127.0.0.1:8000/api/shipments/{shipment.id}/
            """
            
            _send_email(
                subject=subject,
                text_content=message,
                recipient_list=[customer.email] if customer.email else []
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending shipment notification: {str(e)}")
            return False


def _send_email(subject, text_content, html_content=None, recipient_list=None):
    """
    Internal function to send email
    
    Args:
        subject: Email subject
        text_content: Plain text content
        html_content: HTML content (optional)
        recipient_list: List of recipient emails
    """
    if not recipient_list:
        return False
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@safaristores.com',
            to=recipient_list
        )
        
        if html_content:
            email.attach_alternative(html_content, "text/html")
        
        email.send(fail_silently=False)
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False
