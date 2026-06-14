from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.first_name', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True, allow_null=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_name', 'notification_type', 'title', 
                  'message', 'channel', 'order', 'order_number', 'is_read', 'is_sent', 
                  'sent_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
