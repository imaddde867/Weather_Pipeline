# weather_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from web_platform.views import home  # Adjust the import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),  # Include weather app URLs
    path('', home, name='home'),  # Root URL pattern
]
