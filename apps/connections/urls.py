from django.urls import path
from .views import send_request, accept_request, reject_request, connections_list

urlpatterns = [
    path('send/<int:to_user_id>/', send_request, name='send_request'),
    path('accept/<int:request_id>/', accept_request, name='accept_request'),
    path('reject/<int:request_id>/', reject_request, name='reject_request'),
    path('list/', connections_list, name='connections_list'),
]