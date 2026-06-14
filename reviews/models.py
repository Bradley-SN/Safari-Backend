from django.db import models
from authentication.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Product Review and Rating Model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    unhelpful_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'customer')
        indexes = [
            models.Index(fields=['product', 'rating']),
            models.Index(fields=['customer']),
        ]
    
    def __str__(self):
        return f"Review by {self.customer.email} for {self.product.name}"
