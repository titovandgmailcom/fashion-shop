from django.urls import path
from . import views

urlpatterns = [
    path('auth/phone/', views.phone_auth, name='phone-auth'),
    path('auth/register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]