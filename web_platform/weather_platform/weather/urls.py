# weather_platform/weather/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_data, name='weather_data'),  # Point to the weather_data view
]
