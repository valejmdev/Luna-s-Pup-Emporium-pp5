from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total', 'payment_status', 'order_status')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__user__username', 'product__name')
