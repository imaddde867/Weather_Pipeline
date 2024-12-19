# main.py
import requests
import psycopg2
from datetime import datetime, timedelta
from scripts.transform import transform_weather_data
from scripts.load import store_transformed_data_to_db


def get_date_range():
    """
    Generate a date range for the past 7 days.
    Returns:
        tuple: Start and end date in 'YYYY-MM-DD' format.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def fetch_weather_data(api_key, location, date1, date2):
    """
    Fetch weather data from the Visual Crossing API.
    Args:
        api_key (str): API key for authentication.
        location (str): Location for which to fetch the weather.
        date1 (str): Start date in 'YYYY-MM-DD' format.
        date2 (str): End date in 'YYYY-MM-DD' format.
    Returns:
        dict: Parsed JSON data from the API response.
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date1}/{date2}"
    params = {
        "key": api_key,
        "unitGroup": "us",
        "contentType": "json",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP response codes >= 400
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {}

# Main ETL Process
if __name__ == "__main__":
    # Replace with your actual credentials
    api_key = "C6GA33FDG6AAGQ38C38BSYS9W"
    location = "Hann Münden"
    # Automatically generate date range for the past 7 days
    date1, date2 = get_date_range()

    # Fetch the weather data
    data = fetch_weather_data(api_key, location, date1, date2)
    if not data:
        print("Failed to fetch weather data. Exiting ETL process.")
        exit()

    # Transform the data
    transformed_data = transform_weather_data(data)
    if not transformed_data:
        print("Failed to transform weather data. Exiting ETL process.")
        exit()

    try:
        # Set up database connection
        conn = psycopg2.connect(dbname="weather_db", user="admin", password="12345", host="localhost")
        # Store transformed data in the database
        store_transformed_data_to_db(transformed_data, conn)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()
