from django.shortcuts import render
from .models import Weather
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Weather Platform!")

def weather_list(request):
    weather_data = Weather.objects.all()  # Fetch all weather data
    return render(request, 'weather/weather_list.html', {'weather_data': weather_data})