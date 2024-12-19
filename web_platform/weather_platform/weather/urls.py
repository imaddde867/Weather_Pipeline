from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_list, name='weather_list'),
]
