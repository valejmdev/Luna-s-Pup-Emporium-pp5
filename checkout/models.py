from django.contrib.auth import get_user_model
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from store.models import Product

# Get the user model used by Django
User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(
        max_length=32, null=False, editable=False, unique=True)
    full_name = models.CharField(
        max_length=50, null=True, blank=True, default='Unknown')
    email = models.EmailField(
        max_length=254, null=True, blank=True, default='default@example.com')
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, default='')
    country = models.CharField(
        max_length=40, null=True, blank=True, default='Unknown')
    postcode = models.CharField(
        max_length=20, null=True, blank=True)
    town_or_city = models.CharField(
        max_length=40, null=True, blank=True, default='Unknown')
    street_address1 = models.CharField(
        max_length=80, null=True, blank=True, default='')
    street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
         max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update grand total each time a line item is added,
        accounting for delivery costs."""
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override the original save method to set the order number."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
                f"Order {self.id} - "
                f"{self.user.username if self.user else 'Guest'}"
                )


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False)

    def save(self, *args, **kwargs):
        """Override the save method to calculate the lineitem
        total and update the order total."""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
