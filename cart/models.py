from django.db import models
from django.conf import settings
from store.models import Product
from django.core.exceptions import ValidationError


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
         Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Cart {self.cart.id}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
