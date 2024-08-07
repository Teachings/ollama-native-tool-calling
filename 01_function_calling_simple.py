import requests
import json
from weather_tool import get_weather

# Collect tool definitions from decorated functions
tools = [get_weather.tool_definition]

# Define the request payload
payload = {
    "model": "llama3.1:70b", #llama3.1:8b-instruct-q8_0 
    "messages": [
        {
            "role": "system",
            "content": "You are a smart AI assistant. You are a master at understanding what a customer wants and utilize available tools only if you have to."
         },
        {
            "role": "user", 
            "content": "How hot is it in minneapolis??"
        }
    ],
    "tools": tools
}
# Define the OpenAI endpoint and API key
api_url = "http://ai.mtcl.lan:11434/v1/chat/completions"
api_key = "no_api_key_required"

# Make the request to the OpenAI API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
response = requests.post(api_url, headers=headers, data=json.dumps(payload))

print(response.json())

# Handle the tool response
if response.status_code == 200:
    response_data = response.json()
    tool_calls = response_data.get('choices', [{}])[0].get('message', {}).get('tool_calls', [])
    for call in tool_calls:
        if call['type'] == 'function' and call['function']['name'] == 'get_weather':
            location = json.loads(call['function']['arguments'])['location']
            weather = get_weather(location)
            print(f"Weather in {location}: {weather}")
else:
    print(f"Error: {response.status_code}, {response.text}")
