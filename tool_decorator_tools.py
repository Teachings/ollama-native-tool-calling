# convert_tools.py
import random
from tool_decorator import custom_tool

@custom_tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a specified location.
    
    This tool simulates checking the weather by randomly selecting from three possible outcomes: sunny, cold, or rainy. 
    The chance of each outcome is equal (1/3). If the random check fails, it may return an unexpected result to simulate real-world unpredictable conditions.
    
    Args:
        location (str): The name of the location for which to check the weather.
        
    Returns:
        str: A string describing the current weather in the specified location, randomly chosen from three possible outcomes.
    """
    # start a random check for 1/3 of times to simulate a failure
    if random.randint(0, 2) == 0 :
        return "Sunny, 78F"
    elif random.randint(0, 2) == 1:
        return "Cold, 22F"
    else:
        return "Rainy, 60F"

@custom_tool
def get_system_time(location: str = "Minnesota") -> str:
    """Get the current system time. If no location is provided, use default location as 'Woodbury, Minnesota'.
    
    This tool simulates retrieving the system time by randomly selecting from three possible outcomes: morning, afternoon, or evening. 
    The chance of each outcome is equal (1/3). If the random check fails, it may return an unexpected result to simulate real-world unpredictable conditions.
    
    Args:
        location (str): Optional. The name of the location for which to retrieve the system time. It defaults to Minnesota if not provided.  
        
    Returns:
        str: A string describing the current system time in the specified or default location, randomly chosen from three possible outcomes.
    """
    # start a random check for 1/3 of times to simulate a failure
    if random.randint(0, 2) == 0 :
        return "2:00 AM"
    elif random.randint(0, 2) == 1:
        return "3:00 PM"
    else:
        return "6:15 PM"


# # Serialize and validate the JSON
# tool_definition = get_current_weather.tool_definition

# import json
# json_tool_definition = json.dumps(tool_definition, indent=4)
# print(json_tool_definition)

# # Optionally, you can also validate the JSON structure using a JSON schema validator.
# try:
#     json.loads(json_tool_definition)
#     print("The JSON structure is valid.")
# except json.JSONDecodeError as e:
#     print(f"JSON validation error: {e}")
