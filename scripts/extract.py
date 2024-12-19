import requests
import psycopg2
from datetime import datetime, timedelta

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
    Args:å
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


def store_weather_data_to_db(data, conn):
    """
    Store weather data in a PostgreSQL database.
    Args:
        data (dict): Weather data to store.
        conn (psycopg2.connection): PostgreSQL database connection.
    """
    cursor = conn.cursor()

    # Safely access 'currentConditions'
    current_conditions = data.get("currentConditions")
    if not current_conditions:
        print("No 'currentConditions' found in the API response. Skipping insertion.")
        return

    # Get the datetime and handle if it's time-only (HH:MM:SS)
    raw_datetime = current_conditions.get("datetime")
    if not raw_datetime:
        print("No 'datetime' found in current conditions. Skipping insertion.")
        return

    if len(raw_datetime) == 8:  # If it's time-only (HH:MM:SS)
        day_date = data.get('days')[0].get('datetime')  # Get the date from the first day in the response
        if not day_date:
            print("No 'datetime' found for the first day. Skipping insertion.")
            return
        raw_datetime = f"{day_date} {raw_datetime}"  # Combine date and time to make a full timestamp

    try:
        # Insert data into the 'current_conditions' table
        cursor.execute("""
            INSERT INTO current_conditions (
                datetime, temp, feelslike, dew, humidity, pressure, windspeed, windgust, winddir, 
                visibility, cloudcover, precip, precipprob, uvindex, severerisk, conditions, description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            raw_datetime,
            current_conditions.get("temp"),
            current_conditions.get("feelslike"),
            current_conditions.get("dew"),
            current_conditions.get("humidity"),
            current_conditions.get("pressure"),
            current_conditions.get("windspeed"),
            current_conditions.get("windgust"),
            current_conditions.get("winddir"),
            current_conditions.get("visibility"),
            current_conditions.get("cloudcover"),
            current_conditions.get("precip"),
            current_conditions.get("precipprob"),
            current_conditions.get("uvindex"),
            current_conditions.get("severerisk"),
            current_conditions.get("conditions"),
            current_conditions.get("description")
        ))
        conn.commit()
        print("Weather data successfully stored in the database.")
    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")
        conn.rollback()
    finally:
        cursor.close()


# Main ETL Process
if __name__ == "__main__":
    # Replace with your actual credentials
    api_key = "C6GA33FDG6AAGQ38C38BSYS9W"
    location = "Hann Münden"
    # Automatically generate date range for the past 2 days
    date1, date2 = get_date_range()

    # Fetch the weather data
    data = fetch_weather_data(api_key, location, date1, date2)
    if not data:
        print("Failed to fetch weather data. Exiting ETL process.")
        exit()

    try:
        # Set up database connection
        conn = psycopg2.connect(dbname="weather_db", user="admin", password="12345", host="localhost")
        # Store data in the database
        store_weather_data_to_db(data, conn)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()
