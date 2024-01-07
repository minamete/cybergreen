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

def evaluate_idea_impact(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to evaluate the impact of an idea based on the problem, solution, and its category.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Considering the problem and proposed solution, especially in relation to the category '{category}', please analyze the potential impact on environmental, social, and economic aspects.
    """
    
    # Assuming you have a function `get_openai_response` to interact with OpenAI API
    response = get_openai_response(prompt)
    return response


def evaluate_business_risks(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to evaluate the business risks and threats of an idea based on the problem, solution, and its category.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Business Risk Analysis: Considering the above problem and solution, especially in relation to the category '{category}', what could be the potential business risks and threats associated with this solution? Please analyze in terms of market viability, competition, financial stability, and regulatory challenges.
    """
    
    # Assuming you have a function `get_openai_response` to interact with OpenAI API
    response = get_openai_response(prompt)
    return response

def get_market_insights(problem, solution, category):
    """
    Generates prompts for the OpenAI API to obtain insights on market size, biggest competitors, and general market trends for a given solution.
    """
    # Market Size Prompt
    market_size_prompt = f"""
    Analyze the market size for a solution related to '{category}' which addresses the problem: {problem}. The solution proposed is: {solution}. Provide current figures and projected growth.
    """
    
    # Competitors Prompt
    competitors_prompt = f"""
    Identify the biggest competitors in the market for solutions related to '{category}', which addresses the problem: {problem}. The solution proposed is: {solution}. Discuss their strengths and weaknesses.
    """

    # Market Trends Prompt
    market_trends_prompt = f"""
    Discuss the current and emerging trends in the market relevant to '{category}' solutions, particularly those addressing the problem: {problem}. How might these trends impact the future of this market?
    """

    # Assuming you have a function `get_openai_response` to interact with OpenAI API
    market_size_response = get_openai_response(market_size_prompt)
    competitors_response = get_openai_response(competitors_prompt)
    market_trends_response = get_openai_response(market_trends_prompt)

    return {
        "Market Size Analysis": market_size_response,
        "Competitor Analysis": competitors_response,
        "Market Trends Analysis": market_trends_response
    }


def regulatory_compliance_assessment(problem, solution):
    """
    Generate a prompt for evaluating the regulatory and compliance aspects of a solution.
    """
    prompt = f"""
    Considering the problem '{problem}' and the proposed solution '{solution}', 
    what are the regulatory and compliance considerations that need to be addressed? 
    Include potential regulatory challenges and necessary compliance measures.
    """
    # Call the OpenAI API with the prompt
    # response = openai_api_call(prompt)  # Replace with actual API call
    return prompt  # Returning prompt for demonstration

def competitive_advantage_usp(problem, solution):
    """
    Generate a prompt for evaluating the competitive advantage and unique selling proposition of a solution.
    """
    prompt = f"""
    Given the problem '{problem}' and the solution '{solution}', 
    what is the competitive advantage and unique selling proposition (USP) of this solution? 
    Explain how it stands out from competitors and its potential market impact.
    """
    # Call the OpenAI API with the prompt
    # response = openai_api_call(prompt)  # Replace with actual API call
    return prompt  # Returning prompt for demonstration

