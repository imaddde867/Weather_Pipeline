#EXTRACTION
import requests

def fetch_weather_data(api_key, location, date1, date2):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date1}/{date2}"
    params = {
        "key": api_key,
        "unitGroup": "metric",
        "contentType": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

api_key = "C6GA33FDG6AAGQ38C38BSYS9W"
location = "Hann Münden"
date1 = "2024-12-15"
date2 = "2024-12-17"

weather_data = fetch_weather_data(api_key, location, date1, date2)
print(weather_data)