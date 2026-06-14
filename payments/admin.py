from django.contrib import admin
from .models import Payment, PaymentLog


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('transaction_id', 'order__order_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [PaymentLogInline]
    fieldsets = (
        ('Payment Info', {'fields': ('order', 'transaction_id', 'payment_method')}),
        ('Amount & Status', {'fields': ('amount', 'status')}),
        ('Details', {'fields': ('description', 'created_at', 'updated_at')}),
    )


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('payment', 'status', 'response_code', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__transaction_id', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
