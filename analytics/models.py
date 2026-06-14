from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta


class DailySalesReport(models.Model):
    """Daily Sales Report Model"""
    date = models.DateField(unique=True)
    total_orders = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_items_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Sales Report - {self.date}"


class ProductAnalytics(models.Model):
    """Product Performance Analytics"""
    date = models.DateField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    units_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    views_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-revenue']
        unique_together = ('date', 'product_id')
    
    def __str__(self):
        return f"{self.product_name} - {self.date}"


class CustomerAnalytics(models.Model):
    """Customer Activity Analytics"""
    date = models.DateField()
    total_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    new_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    returning_customers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_cart_abandonment = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Customer Analytics'
    
    def __str__(self):
        return f"Customer Analytics - {self.date}"


class StockAlerts(models.Model):
    """Low Stock Alerts for Admin"""
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(validators=[MinValueValidator(0)])
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Low Stock: {self.product_name}"
