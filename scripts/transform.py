def transform_weather_data(data):
    """
    Transform and clean the weather data from the API.
    Args:
        data (dict): Raw weather data from the API.
    Returns:
        dict: Transformed weather data ready for insertion into the database.
    """
    transformed_data = {}

    # Transform current conditions
    current_conditions = data.get("currentConditions", {})
    if current_conditions:
        transformed_data['current_conditions'] = {
            "datetime": current_conditions.get("datetime"),
            "temp": current_conditions.get("temp"),
            "feelslike": current_conditions.get("feelslike"),
            "dew": current_conditions.get("dew"),
            "humidity": current_conditions.get("humidity"),
            "pressure": current_conditions.get("pressure"),
            "windspeed": current_conditions.get("windspeed"),
            "windgust": current_conditions.get("windgust"),
            "winddir": current_conditions.get("winddir"),
            "visibility": current_conditions.get("visibility"),
            "cloudcover": current_conditions.get("cloudcover"),
            "precip": current_conditions.get("precip"),
            "precipprob": current_conditions.get("precipprob"),
            "uvindex": current_conditions.get("uvindex"),
            "severerisk": current_conditions.get("severerisk"),
            "conditions": current_conditions.get("conditions"),
            "description": current_conditions.get("description"),
        }

    # Transform hourly data
    hours = []
    for day in data.get('days', []):
        for hour in day.get('hours', []):
            hours.append({
                "datetime": hour.get("datetime"),
                "temp": hour.get("temp"),
                "feelslike": hour.get("feelslike"),
                "windspeed": hour.get("windspeed"),
                "windgust": hour.get("windgust"),
                "winddir": hour.get("winddir"),
                "precip": hour.get("precip"),
                "precipprob": hour.get("precipprob"),
                "humidity": hour.get("humidity"),
                "visibility": hour.get("visibility"),
                "cloudcover": hour.get("cloudcover"),
                "pressure": hour.get("pressure"),
            })

    transformed_data['hourly'] = hours

    # Alerts data transformation (if any)
    alerts = []
    for alert in data.get("alerts", []):
        alerts.append({
            "event": alert.get("event"),
            "description": alert.get("description"),
            "expires": alert.get("expires")
        })

    transformed_data['alerts'] = alerts

    return transformed_data
