import requests
import json
from weather_tool import get_weather
from termcolor import colored

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

# Define a dictionary of tool functions
tool_functions = {
    "get_weather": get_weather
}

SYSTEM_MESSAGE_CONTENT = "You are a smart AI assistant. \
    You are a master at understanding what a user wants and utilize available tools only if you have to.  \
    If you utilize a tool call's answer in your final reply \
        you always let user know that you used a tool call response and did not make up the answer by yourself.\
    If you used more than one tool call responses for your final answer, then highlight that too."

USER_MESSAGE_CONTENT = "Is it hotter in New Delhi or in Minneapolis? How hot is it? I want to plan a visit to the cooler place."

model = "llama3.1:70b"
messages = [
    {
        "role": "system", 
        "content": SYSTEM_MESSAGE_CONTENT
    },
    {
        "role": "user", 
        "content": USER_MESSAGE_CONTENT
    }
]

# Define the request payload
payload = {
    "model": model,
    "messages": messages,
    "tools": tools
}

# Print the initial request payload
print(colored("Initial Request Payload:", "cyan"))
print(colored(json.dumps(payload, indent=2), "yellow"))

response = requests.post(api_url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    response_data = response.json()
    
    # Print the initial response
    print(colored("Initial Response:", "cyan"))
    print(colored(json.dumps(response_data, indent=2), "green"))
    
    tool_calls = response_data.get('choices', [{}])[0].get('message', {}).get('tool_calls', [])

    # Initialize an empty array (list) to store tool messages
    tool_messages = []

    # Iterate over all tool calls to construct tool messages
    for call in tool_calls:
        tool_call_id = call['id']
        function_name = call['function']['name']
        tool_function = tool_functions.get(function_name)
        
        if tool_function:
            arguments = json.loads(call['function']['arguments'])
            result = tool_function(**arguments)
            print(colored(f"Result from {function_name}: {result}", "magenta"))

            # Construct the tool message using the tool's function details
            tool_message = {
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call_id
            }
            # Append the constructed tool message to the array (list)
            tool_messages.append(tool_message)
        else:
            print(colored(f"No tool function found for {function_name}", "red"))

else:
    print(colored(f"Error: {response.status_code}, {response.text}", "red"))

# Extend messages with tool responses only if there were successful tool calls
if tool_messages:
    messages.extend(tool_messages)

# Prepare the final payload with updated messages
payload = {
    "model": model,
    "messages": messages,
    "tools": tools
}

# Print the final request payload
print(colored("Final Request Payload:", "cyan"))
print(colored(json.dumps(payload, indent=2), "yellow"))

# Make the final request to the OpenAI API
final_response = requests.post(api_url, headers=headers, data=json.dumps(payload))

if final_response.status_code == 200:
    final_response_data = final_response.json()
    
    # Print the final response
    print(colored("Final Response:", "cyan"))
    final_content = final_response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
    print(colored(final_content, "green"))
else:
    print(colored(f"Error: {final_response.status_code}, {final_response.text}", "red"))
