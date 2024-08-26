from django.urls import path
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.index, name='index'),
    path('all-products/', views.all_products, name='all_products'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('special-offers/', views.special_offers, name='special_offers'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
]