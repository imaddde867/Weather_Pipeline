from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported
from weather.views import home  # Import your home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),  # Include weather app URLs
    path('', home, name='home'),  # Root URL pattern
]
