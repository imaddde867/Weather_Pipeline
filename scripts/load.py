import psycopg2

def store_transformed_data_to_db(transformed_data, conn):
    """
    Store transformed weather data in the database.
    Args:
        transformed_data (dict): Transformed weather data.
        conn (psycopg2.connection): Database connection.
    """
    cursor = conn.cursor()

    # Store current conditions
    current_conditions = transformed_data.get('current_conditions', {})
    if current_conditions:
        cursor.execute("""
            INSERT INTO current_conditions (
                datetime, temp, feelslike, dew, humidity, pressure, windspeed, windgust, winddir, 
                visibility, cloudcover, precip, precipprob, uvindex, severerisk, conditions, description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            current_conditions['datetime'],
            current_conditions['temp'],
            current_conditions['feelslike'],
            current_conditions['dew'],
            current_conditions['humidity'],
            current_conditions['pressure'],
            current_conditions['windspeed'],
            current_conditions['windgust'],
            current_conditions['winddir'],
            current_conditions['visibility'],
            current_conditions['cloudcover'],
            current_conditions['precip'],
            current_conditions['precipprob'],
            current_conditions['uvindex'],
            current_conditions['severerisk'],
            current_conditions['conditions'],
            current_conditions['description']
        ))

    # Store hourly data
    hourly_data = transformed_data.get('hourly', [])
    for hour in hourly_data:
        cursor.execute("""
            INSERT INTO hourly_weather (
                datetime, temp, feelslike, windspeed, windgust, winddir, precip, precipprob, humidity, 
                visibility, cloudcover, pressure
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            hour['datetime'],
            hour['temp'],
            hour['feelslike'],
            hour['windspeed'],
            hour['windgust'],
            hour['winddir'],
            hour['precip'],
            hour['precipprob'],
            hour['humidity'],
            hour['visibility'],
            hour['cloudcover'],
            hour['pressure']
        ))

    # Store alerts data
    alerts_data = transformed_data.get('alerts', [])
    for alert in alerts_data:
        cursor.execute("""
            INSERT INTO weather_alerts (
                event, description, expires
            )
            VALUES (%s, %s, %s)
        """, (
            alert['event'],
            alert['description'],
            alert['expires']
        ))

    conn.commit()
    print("Transformed weather data successfully stored in the database.")
    cursor.close()
