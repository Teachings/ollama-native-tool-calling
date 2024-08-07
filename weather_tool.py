import requests
from tool_decorator import custom_tool
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Constants
API_KEY = os.getenv('VISUAL_CROSSING_API_KEY')  # Replace with your actual API key
UNIT_GROUP = 'us'
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
            f"Current temperature is {today_weather['temp']}°F (feels like {today_weather['feelslike']}°F) with "
            f"high of {today_weather['tempmax']}°F and low of {today_weather['tempmin']}°F\n"
            f"Precipitation probability is {today_weather['precipprob']}% and "
            f"humidity is {today_weather['humidity']}%\n"
            f"Wind speed: {today_weather['windspeed']} km/h (gusts up to {today_weather['windgust']} km/h)\n"
            f"UV index: {today_weather['uvindex']}\n"
            f"Sunrise is at {today_weather['sunrise']} and sunset is at {today_weather['sunset']}"
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