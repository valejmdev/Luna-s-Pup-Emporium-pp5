from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.profile, name='profile'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
]