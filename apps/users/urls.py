from django.urls import path
from .views import search, edit_profile, register

urlpatterns = [
    path('search/', search, name='search'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('accounts/register/', register, name='register'),
]