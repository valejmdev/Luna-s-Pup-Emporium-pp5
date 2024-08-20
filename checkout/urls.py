from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),  
]