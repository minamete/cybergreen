from dotenv import load_dotenv
import os
from openai import OpenAI

from train_lda_model import run_lda_training

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

# ---------------------------------------------------------------------
# EVALUATION PROMPTS

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
   
    response = get_openai_response(prompt) 
    return response 

def competitive_advantage_usp(problem, solution):
    """
    Generate a prompt for evaluating the competitive advantage and unique selling proposition of a solution.
    """
    prompt = f"""
    Given the problem '{problem}' and the solution '{solution}', 
    what is the competitive advantage and unique selling proposition (USP) of this solution? 
    Explain how it stands out from competitors and its potential market impact.
    """
   
    response = get_openai_response(prompt)  
    return response  

def evaluate_solution_feasibility(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to evaluate the feasibility of a solution and identify potential issues.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Feasibility Analysis: Considering the solution '{solution}' for the problem '{problem}', 
    especially in relation to the category '{category}', assess the feasibility of this solution. 
    Discuss any challenges or issues that might make the solution unfeasible or difficult to implement.
    """
    response = get_openai_response(prompt)
    return response

def identify_funding_resources(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to identify potential government and private funding resources for a business idea.
    """
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Based on this business idea, which focuses on addressing '{problem}' with the solution '{solution}' in the category of '{category}', what are the potential government and private funding resources available? Please provide information on relevant grants, investors, and funding programs that could support this type of initiative.
    """
    response = get_openai_response(prompt)
    return response

# ---------------------------------------------------------------------
# OVERALL WORKFLOW

dataset = "dataset.csv"
interpreted_topics_resp = ""

# Use OpenAI API to interpret topics using trained LDA model output
def get_interpret_prompt():
    lda_output_string = run_lda_training(dataset)
    custom_interpret_instructions = """
    Please provide a brief interpretation of the topics based on this trained LDA model output. Each individual topic should clearly identify a distinct domain or industry. Together, the topics should comprehensively cover the concept of the circular economy, which focuses on reusing and recycling resources to minimize waste. Your interpretation of the topics will be used to classify new problem and solution pairs to the most descriptive and accurate ability. Keep in mind that is the option to classify as "Other" if there is no one topic is sufficient. Format your response as separate lines of Topic X: Name. 

    Here is an example. Given the following,

    Topic 1: 0.031*"food" + 0.009*"business" + 0.008*"system" + 0.007*"local" + 0.007*"container" + 0.007*"community" + 0.006*"material" + 0.006*"product" + 0.006*"recycling" + 0.005*"space"
    Topic 2: 0.018*"model" + 0.012*"fashion" + 0.011*"product" + 0.010*"consumer" + 0.010*"new" + 0.010*"industry" + 0.009*"material" + 0.009*"resource" + 0.009*"recycling" + 0.008*"business"
    Topic 3: 0.013*"paper" + 0.010*"energy" + 0.008*"product" + 0.008*"carbon" + 0.006*"process" + 0.006*"emission" + 0.006*"material" + 0.005*"need" + 0.005*"reduce" + 0.005*"environment"
    Topic 4: 0.034*"plastic" + 0.026*"packaging" + 0.009*"product" + 0.008*"system" + 0.008*"business" + 0.008*"material" + 0.007*"use" + 0.007*"recycling" + 0.006*"singleuse" + 0.006*"container"
    Topic 5: 0.019*"energy" + 0.011*"resource" + 0.010*"system" + 0.010*"use" + 0.008*"sustainable" + 0.007*"product" + 0.007*"business" + 0.006*"reduce" + 0.006*"company" + 0.005*"vehicle"
    Topic 6: 0.018*"material" + 0.011*"construction" + 0.010*"industry" + 0.007*"new" + 0.006*"cost" + 0.006*"resource" + 0.006*"building" + 0.006*"use" + 0.005*"process" + 0.005*"need"

    The topics that could be interpreted are:
    Topic 1: Food and Agriculture Systems
    Topic 2: Fashion and Consumer
    Topic 3: Energy and Emissions
    Topic 4: Packaging and Single-Use Materials
    Topic 5: Resource Management
    Topic 6: Infrastructure and Construction
    """
    return lda_output_string + "\n" + custom_interpret_instructions

def get_interpreted_topics(): 
    interpret_prompt = get_interpret_prompt()
    interpreted_topics_resp = get_openai_response(interpret_prompt)

# Use OpenAI API to classify new user input
def predict_topic(user_input): 
    # Strip user input to get problem and solution
    user_problem = "Sample problem text"
    user_solution = "Sample solution text"

    predict_topic_prompt = """
    An individual has submitted a circular economy business idea.

    Problem: f{user_problem}
    Solution: f{user_solution}

    Recall the topics which can be used for classification: f{interpreted_topics_string}.
    Predict the relevant topic of the new idea. Respond in one concise sentence with the most likely topic name, your level of confidence in that classification, and a brief description in how you know that the idea can contribute to innovation in that topic. If you are not confident that any topic is appropriate, say "Other," and concisely explain your reasoning.
    """

    predicted_topic_resp = get_openai_response(predict_topic_prompt)

# Augmenting the user input with the predicted topic

# Test usage here
user_input = "what are 10 commonly discussed solutions to combat plastic waste"
response = get_openai_response(user_input)
print("Assistant:", response)