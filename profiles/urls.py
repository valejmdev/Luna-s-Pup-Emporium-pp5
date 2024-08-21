from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<str:username>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),

]