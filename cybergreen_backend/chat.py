from dotenv import load_dotenv
import os
from openai import OpenAI

from train_lda_model import run_lda_training

dataset = "dataset.csv"

# IN PROGRESS
def interpret_topics():
    # Interpret topics using ChatGPT using concatenated data
    lda_output_string = run_lda_training(dataset)

    interpret_prompt = lda_output_string + "\n" + "Please provide a brief interpretation of the topics."

    # Use API to interpret the topics 

# IN PROGRESS
def predict_topic(user_input): 
    # Example prompt for classifying new data
    new_data_prompt = """
    Problem: [New Problem Text]
    Solution: [New Solution Text]
    Interpretation: [ChatGPT interpretation of topics]
    What topic does this new data align with?
    """

    # Use API to predict the relevant topic of new data
    

# Augment input to ChatGPT with predicted topic

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

def evaluate_idea_impact(problem, solution):
    """
    Generates a prompt for the OpenAI API to evaluate the impact of an idea based on the problem, solution, and its category.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Considering the problem and proposed solution, please analyze the potential impact of the business on environmental, social, and economic aspects.
    """

    response = get_openai_response(prompt)
    return response

# Example usage
problem_example = "High levels of food waste in urban areas"
solution_example = "Implementing a city-wide composting program"

# Get the OpenAI API response
impact_analysis = evaluate_idea_impact(problem_example, solution_example)
print("Impact Analysis:", impact_analysis)


# Example usage
user_input = "what are 10 commonly discussed solutions to combat plastic waste"
response = get_openai_response(user_input)
print("Assistant:", response)
