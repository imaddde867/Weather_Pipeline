# weather_platform/weather_platform/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Default home page
    path('weather/', include('weather.urls')),  # Weather app URLs
]
