# Weather Data Platform

This project involves building a weather data platform that collects weather data from the **Visual Crossing** API, processes it using an ETL pipeline, and presents it through a Django web application. The platform allows users to view real-time weather data and explore the ETL process used to collect and transform the data.

![Alt text](https://github.com/imaddde867/Weather_Pipeline/blob/main/web_platform/preview.png)

## Table of Contents

- [Overview](#overview)
- [API Integration](#api-integration)
- [ETL Pipeline](#etl-pipeline)
- [Web Interface](#web-interface)
- [Database Schema](#database-schema)
- [Running the Project Locally](#running-the-project-locally)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)

## Overview

This project is designed to showcase a complete weather data pipeline, which includes:

1. **API Integration**: Fetching weather data from the Visual Crossing API.
2. **ETL Pipeline**: Extracting, transforming, and loading (ETL) the weather data into a PostgreSQL database.
3. **Web Interface**: A Django-based web interface that allows users to visualize the weather data.

## API Integration

The weather data is fetched from the **Visual Crossing** API, which provides real-time weather data, including:

- Location (city or region)
- Temperature
- Humidity
- Weather conditions
- Date and time of the data

The API is integrated into the backend of the platform using the `requests` Python library. Data fetched from the API is then processed and stored in the database through the ETL pipeline.

### Visual Crossing API

The API URL looks like this:

```
https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}
```

Where `{location}` can be the city or region, and `{api_key}` is your Visual Crossing API key.

The data returned from the API contains multiple weather parameters, including temperature, precipitation, humidity, and more.

## ETL Pipeline

The ETL pipeline is responsible for:

1. **Extracting** weather data from the Visual Crossing API.
2. **Transforming** the data by cleaning it and ensuring it’s in a suitable format (e.g., handling missing values, converting units, etc.).
3. **Loading** the transformed data into a PostgreSQL database for future use.

### Steps in the ETL Process:

1. **Extract**:
   - Data is fetched from the Visual Crossing API at regular intervals (e.g., hourly, daily).
   
2. **Transform**:
   - The fetched data is processed:
     - Temperature units are converted if necessary.
     - Missing values or incorrect data formats are handled.
     - Data is structured in a way that makes it easy to store in a database.
   
3. **Load**:
   - The transformed data is loaded into a PostgreSQL database. A model `Weather` is used to store details such as location, temperature, humidity, and date-time.

## Database Schema

The following database schema is used to store the weather data:
![alt text](https://github.com/imaddde867/Weather_Pipeline/blob/main/Database_Preview.png)

### `locations` Table

Stores information about each location.

```sql
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    resolved_address VARCHAR(255),
    address VARCHAR(255),
    timezone VARCHAR(100),
    tzoffset INT
);
```

### `current_conditions` Table

Stores current weather conditions for each location.

```sql
CREATE TABLE current_conditions (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(id),
    datetime TIMESTAMP,
    temp FLOAT,
    feelslike FLOAT,
    dew FLOAT,
    humidity INT,
    pressure INT,
    windspeed FLOAT,
    windgust FLOAT,
    winddir INT,
    visibility FLOAT,
    cloudcover INT,
    precip FLOAT,
    precipprob INT,
    uvindex INT,
    severerisk INT,
    conditions TEXT,
    description TEXT
);
```

### `daily_forecast` Table

Stores the daily weather forecast for each location.

```sql
CREATE TABLE daily_forecast (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(id),
    datetime DATE,
    tempmax FLOAT,
    tempmin FLOAT,
    temp FLOAT,
    dew FLOAT,
    feelslike FLOAT,
    precip FLOAT,
    precipprob INT,
    precipcover INT,
    preciptype TEXT,
    snow FLOAT,
    snowdepth FLOAT,
    windspeed FLOAT,
    windgust FLOAT,
    winddir INT,
    visibility FLOAT,
    cloudcover INT,
    pressure INT,
    solarradiation FLOAT,
    solarenergy FLOAT,
    uvindex INT,
    severerisk INT,
    sunrise TIME,
    sunset TIME,
    moonphase TEXT,
    icon TEXT,
    conditions TEXT,
    description TEXT
);
```

### `hourly_forecast` Table

Stores hourly weather data for each daily forecast.

```sql
CREATE TABLE hourly_forecast (
    id SERIAL PRIMARY KEY,
    daily_forecast_id INT REFERENCES daily_forecast(id),
    datetime TIME,
    temp FLOAT,
    dew FLOAT,
    feelslike FLOAT,
    precip FLOAT,
    windspeed FLOAT,
    windgust FLOAT,
    winddir INT,
    visibility FLOAT,
    cloudcover INT,
    humidity INT,
    pressure INT
);
```

### `alerts` Table

Stores weather alerts for each location.

```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(id),
    event VARCHAR(100),
    description TEXT
);
```

## Web Interface

The web interface is built using the Django web framework. The app allows users to:

- View the weather data from the database.
- Visualize the data in an easy-to-read format.

### Key Components of the Web Interface:

1. **Home Page**: A welcoming page with information about the project, including the Visual Crossing API, the ETL process, and the weather app.
2. **Weather Data Page**: Displays weather data in a table, including columns for location, temperature, humidity, and timestamp.
3. **Interactive Features**: Future features may include filtering data by location, date range, or weather conditions.

### Example `views.py` for the Web Interface

```python
from django.shortcuts import render
from .models import Weather

def weather_data(request):
    weather_data = Weather.objects.all()  # Fetch weather data from the database
    return render(request, 'weather/weather_data.html', {'weather': weather_data})
```

### Example `weather_data.html` Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Data</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Weather Data</h1>
    <table>
        <thead>
            <tr>
                <th>Location</th>
                <th>Temperature (°C)</th>
                <th>Humidity (%)</th>
                <th>Date and Time</th>
            </tr>
        </thead>
        <tbody>
            {% for weather_item in weather %}
                <tr>
                    <td>{{ weather_item.location }}</td>
                    <td>{{ weather_item.temperature }}°C</td>
                    <td>{{ weather_item.humidity }}%</td>
                    <td>{{ weather_item.date_time }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

## Running the Project Locally

To run this project on your local machine, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/weather-platform.git
    cd weather-platform
    ```

2. **Set up a virtual environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your PostgreSQL database** (if not done already):
   - Create a database (e.g., `weather_db`) in PostgreSQL.
   - Update your `settings.py` file with the correct database connection details.

5. **Run migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Start the server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the app**:
    - Open your browser and visit `http://127.0.0.1:8000/weather/` to view the weather data.

## Project Structure

```
weather_platform/
│
├── weather_platform/  # Main project directory
│   ├── settings.py    # Django settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI application
│
├── weather/           # Weather app directory
│   ├── migrations/    # Database migrations
│   ├── models.py      # Weather model
│   ├── views.py       # View for weather data
│   ├── templates/     # HTML templates
│   │   └── weather/
│   │       └── weather_data.html
│   ├── urls.py        # URL routing for weather app
│   └── admin.py       # Admin configuration
│
└── requirements.txt   # List of project dependencies
```

## Technologies Used

- Django: A Python web framework for building the web interface.
- PostgreSQL: A relational database for storing weather data.
- Visual Crossing API: A weather API for fetching real-time weather data.
- Python: Programming language used for backend and ETL pipeline.
- requests: Python library for making HTTP requests to the Visual Crossing API.
- pandas: Python library for data manipulation and analysis.
- numpy: Python library for numerical computations
