from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator


class Inventory(models.Model):
    """Stock/Inventory Management Model"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    reserved_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(validators=[MinValueValidator(0)])
    last_restocked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Inventory'
    
    def __str__(self):
        return f"Inventory: {self.product.name}"
    
    @property
    def available_stock(self):
        reserved = self.reserved_stock if self.reserved_stock is not None else 0
        current = self.current_stock if self.current_stock is not None else 0
        return current - reserved
    
    @property
    def low_stock_alert(self):
        reorder = self.reorder_level if self.reorder_level is not None else 0
        return self.available_stock <= reorder


class StockAdjustment(models.Model):
    """Track stock adjustments"""
    ADJUSTMENT_TYPE_CHOICES = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_adjustments')
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPE_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.adjustment_type}: {self.quantity} units of {self.product.name}"
