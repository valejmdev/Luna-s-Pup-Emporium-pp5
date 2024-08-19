from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('products/', views.product_list, name='product_list'),  
    path('products/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),  
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  
    path('faq/', views.faq, name='faq'),  
    path('about/', views.about_us, name='about_us'),  
]