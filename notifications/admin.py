from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'channel', 'is_read', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'channel', 'is_read', 'is_sent', 'created_at')
    search_fields = ('recipient__email', 'subject', 'message')
    readonly_fields = ('created_at', 'sent_at')
    ordering = ('-created_at',)
