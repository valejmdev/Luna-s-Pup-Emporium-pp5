from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email',
                    'phone_number', 'order_total', 'grand_total', 'date')
    search_fields = ('order_number', 'full_name', 'email')
