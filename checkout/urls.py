from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('order_confirmation/<order_number>/', views.order_confirmation, name='order_confirmation'),
]
