import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

user_message = "hello there!"

# Create a list of messages with the user message
messages = [
    {"role": "user", "content": user_message}
]

# Call OpenAI API for completions
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Extract and print the assistant's reply
assistant_reply = response['choices'][0]['message']['content']
print("Assistant:", assistant_reply)
