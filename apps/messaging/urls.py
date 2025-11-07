from django.urls import path
from .views import message_list

urlpatterns = [
    path('<int:user_id>/', message_list, name='message_list'),
]