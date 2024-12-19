# weather_platform/home/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')
