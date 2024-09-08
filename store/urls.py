from django.urls import path
from . import views
from django.conf.urls import handler403, handler404, handler500

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('all-products/', views.all_products, name='all_products'),
    path(
        'category/<slug:category_slug>/',
        views.product_list,
        name='product_list'
    ),
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path('special-offers/', views.special_offers, name='special_offers'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy_policies/', views.privacy_policies, name='privacy_policies'),
    path('faq/', views.faq, name='faq'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
]

handler403 = 'store.views.error_403'
handler404 = 'store.views.error_404'
handler500 = 'store.views.error_500'
