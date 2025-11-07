from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/search/'), name='home'),  # Add this for root redirect
    path('', include('apps.users.urls')),  # Note: You have two '' paths; merge if needed
    path('connections/', include('apps.connections.urls')),
    path('messages/', include('apps.messaging.urls')),
]