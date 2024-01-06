from dotenv import load_dotenv
import os
from openai import OpenAI

from lda_helper import load_lda_model, classify_new_input

# Load pre-trained LDA model
lda_model_path = "models/lda_model"
loaded_lda_model = load_lda_model(lda_model_path)

def predict_topic(user_input):
    # Define human-readable topic labels based on trained LDA model
    topic_labels = {
        0: "Sustainable Packaging",
        1: "Waste Reduction",
        2: "Sustainable Fashion",
        3: "Circular Economy",
        4: "Electronic Waste",
        # Add more as needed
    }

    return classify_new_input(loaded_lda_model, user_input, topic_labels)

def get_openai_response(user_input):

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    # Check if the API key is available
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Create a list of messages with the user message
    messages = [{"role": "user", "content": user_input}]

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

    # Extract and return the assistant's reply
    assistant_reply = response.choices[0].message.content
    return assistant_reply

# Example usage
user_input = "what are 10 commonly discussed solutions to combat plastic waste"
response = get_openai_response(user_input)
print("Assistant:", response)
