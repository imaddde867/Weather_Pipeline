# weather_platform/weather/views.py
from django.shortcuts import render
from .models import Weather  # Import your Weather model

def weather_data(request):
    # Fetch all weather data from the database
    weather_data = Weather.objects.all()
    return render(request, 'weather/weather_data.html', {'weather': weather_data})
