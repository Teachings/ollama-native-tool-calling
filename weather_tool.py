import requests
from tool_decorator import custom_tool


# Constants
API_KEY = ''  # Replace with your actual API key
UNIT_GROUP = 'metric'
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

@custom_tool
def get_weather(location) -> str:
    """Get the current weather in a specified location.    
    Args:
        location (str): The name of the location for which to check the weather in City, State format. 
        
    Returns:
        str: A string describing the current weather in the specified location.
    """
    params = {
        'unitGroup': UNIT_GROUP,
        'key': API_KEY,
        'contentType': 'json'
    }

    try:
        response = requests.get(f"{BASE_URL}{location}", params=params)
        response.raise_for_status()  # Raise an exception if the request fails
        weather_data = response.json()

        today_weather = weather_data['days'][0]

        fun_response = (
            f"Here's the weather for {weather_data['resolvedAddress']} today:\n\n"
            f"{today_weather['description']}\n"
            f"Current temperature: {today_weather['temp']}°C (feels like {today_weather['feelslike']}°C)\n"
            f"High: {today_weather['tempmax']}°C, Low: {today_weather['tempmin']}°C\n"
            f"Precipitation probability: {today_weather['precipprob']}% ({', '.join(today_weather['preciptype'])})\n"
            f"Humidity: {today_weather['humidity']}%\n"
            f"Wind speed: {today_weather['windspeed']} km/h (gusts up to {today_weather['windgust']} km/h)\n"
            f"Cloud cover: {today_weather['cloudcover']}%\n"
            f"UV index: {today_weather['uvindex']}\n"
            f"Sunrise: {today_weather['sunrise']}, Sunset: {today_weather['sunset']}"
        )
        return fun_response
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching the weather data: {e}")
        return None

# Example usage
# location = 'Woodbury, MN'
# weather_info = get_weather(location)
# if weather_info:
#     print(f"Weather description for {location}:")
#     print(weather_info)