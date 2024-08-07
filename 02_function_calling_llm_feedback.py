import requests
import json
from weather_tool import get_weather

# Define the OpenAI endpoint and API key
api_url = "http://ai.mtcl.lan:11434/v1/chat/completions"
api_key = "no_api_key_required"

# Make the request to the OpenAI API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Collect tool definitions from decorated functions
tools = [get_weather.tool_definition]

model = "llama3.1:70b" #llama3.1:8b-instruct-q8_0
messages = [
    {
        "role": "system", 
        "content": "You are a smart AI assistant. You are a master at understanding what a customer wants and utilize available tools only if you have to."
    },
    {
        "role": "user", 
        "content": "Is it hotter in New Delhi or in Minneapolis?"
    }
]

# Define the request payload
payload = {
    "model": model,
    "messages": messages,
    "tools": tools
}

response = requests.post(api_url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    response_data = response.json()
    tool_calls = response_data.get('choices', [{}])[0].get('message', {}).get('tool_calls', [])

    # Initialize an empty array (list) to store tool messages
    tool_messages = []

    # Iterate over all tool calls to construct tool messages
    for call in tool_calls:
        tool_call_id = call['id']
        weather = None
        if call['type'] == 'function' and call['function']['name'] == 'get_weather':
            location = json.loads(call['function']['arguments'])['location']
            weather = get_weather(location)
            print(f"Weather in {location}: {weather}")

        if weather is not None:
            # Construct the tool message using the tool's function details if needed
            tool_message = {
                "role": "tool",
                "content": weather,
                "tool_call_id": tool_call_id
            }
            # Append the constructed tool message to the array (list)
            tool_messages.append(tool_message)
else:
    print(f"Error: {response.status_code}, {response.text}")

# Extend messages with tool responses only if there were successful tool calls
if tool_messages:
    messages.extend(tool_messages)

# Prepare the final payload with updated messages
payload = {
    "model": model,
    "messages": messages,
    "tools": tools
}

# Make the final request to the OpenAI API
final_response = requests.post(api_url, headers=headers, data=json.dumps(payload))

print(final_response.json())
