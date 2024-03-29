from dotenv import load_dotenv
import os
from openai import OpenAI
import re

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
        temperature=0.6,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and return the assistant's reply
    assistant_reply = response.choices[0].message.content
    return assistant_reply

# ---------------------------------------------------------------------
# EVALUATION PROMPTS

def get_base_eval(problem, solution, category):
    """
    Generates a prompt that provides an overview of the feasibility and competitive advantages of a business.
    The prompt also guides the user to click on buttons for more detailed information.
    """
    prompt = f"""
    We're evaluating a business idea in the '{category}' category, aimed at addressing the problem: '{problem}'. The proposed solution is: '{solution}'. 
    Could you analyze and provide insights into the competitive advantages of this business idea? Additionally, assess the feasibility of the business goals, considering the alignment with current market trends and technological capabilities.

    For a more comprehensive understanding of this business idea, including its market potential, risks, and strategic advantages, users are encouraged to explore further detailed analyses.
    Your response should be at most 200 words, make it precise and informative.  
    """
    response = get_openai_response(prompt)
    return response

def get_impact_eval(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to evaluate the impact of an idea based on the problem, solution, and its category.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Considering the problem and proposed solution, especially in relation to the category '{category}', please analyze the potential impact on environmental, social, and economic aspects.
    Your response should be at most 200 words, make it precise and informative.  
    """
    response = get_openai_response(prompt)
    return response

def get_risks_eval(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to evaluate the business risks and threats of an idea based on the problem, solution, and its category.
    """
    # Constructing the prompt
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Business Risk Analysis: Considering the above problem and solution, especially in relation to the category '{category}', what could be the potential business risks and threats associated with this solution? Please analyze in terms of market viability, competition, financial stability, and regulatory challenges.
    Your response should be at most 200 words, make it precise and informative.  
    """
    response = get_openai_response(prompt)
    return response

def get_market_eval(problem, solution, category):
    """
    Generates prompts for the OpenAI API to obtain insights on market size, biggest competitors, and general market trends for a given solution.
    """
    # Market Size Prompt
    market_size_prompt = f"""
    Analyze the market size for a solution related to '{category}' which addresses the problem: {problem}. The solution proposed is: {solution}. Provide current figures and projected growth.
    Your response should be at most 150 words, make it precise and informative.  
    """
    
    # Competitors Prompt
    competitors_prompt = f"""
    Identify the biggest competitors in the market for solutions related to '{category}', which addresses the problem: {problem}. The solution proposed is: {solution}. Discuss their strengths and weaknesses.
    Your response should be at most 150 words, make it precise and informative.  
    """

    # Market Trends Prompt
    market_trends_prompt = f"""
    Discuss the current and emerging trends in the market relevant to '{category}' solutions, particularly those addressing the problem: {problem}. How might these trends impact the future of this market?
    Your response should be at most 150 words, make it precise and informative.  
    """

    market_size_response = get_openai_response(market_size_prompt)
    competitors_response = get_openai_response(competitors_prompt)
    market_trends_response = get_openai_response(market_trends_prompt)

    response = market_size_response + competitors_response + market_trends_response
    return response

def get_regulation_eval(problem, solution):
    """
    Generate a prompt for evaluating the regulatory and compliance aspects of a solution.
    """
    prompt = f"""
    Considering the problem '{problem}' and the proposed solution '{solution}', 
    what are the regulatory and compliance considerations that need to be addressed? 
    Include potential regulatory challenges and necessary compliance measures.
    Your response should be at most 200 words, make it precise and informative.  
    """
   
    response = get_openai_response(prompt) 
    return response 

def get_competition_eval(problem, solution):
    """
    Generate a prompt for evaluating the competitive advantage and unique selling proposition of a solution.
    """
    prompt = f"""
    Given the problem '{problem}' and the solution '{solution}', 
    what is the competitive advantage and unique selling proposition (USP) of this solution? 
    Explain how it stands out from competitors and its potential market impact.
    Your response should be at most 200 words, make it precise and informative.  
    """
   
    response = get_openai_response(prompt)  
    return response  

def get_feasibility_eval(problem, solution, category):
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
    Your response should be at most 200 words, make it precise and informative.  
    """
    response = get_openai_response(prompt)
    return response

def get_funding_eval(problem, solution, category):
    """
    Generates a prompt for the OpenAI API to identify potential government and private funding resources for a business idea.
    """
    prompt = f"""
    Problem: {problem}
    Solution: {solution}
    Predicted Category: {category}
    Based on this business idea, which focuses on addressing '{problem}' with the solution '{solution}' in the category of '{category}', what are the potential government and private funding resources available? Please provide information on relevant grants, investors, and funding programs that could support this type of initiative.
    Your response should be at most 200 words, make it precise and informative.  
    """
    response = get_openai_response(prompt)
    return response

# ---------------------------------------------------------------------
# SCORING PROMPTS

def get_feasibility_score(problem, solution, category):
    """
    Generates a prompt for an AI model to output a feasibility score from 1 to 10 for a business,
    based on the provided problem, solution, and category. Includes examples for training.
    """
    prompt = f"""
    Assess the feasibility of business ideas based on their problems, solutions, and categories. Rate them on a scale from 1 to 10, where 10 is highly feasible. Here are some examples for training:

    Example 1:
    Problem: On a global scale, massive amounts of food gets wasted at a shocking rate. This is particularly prominent in the restaurant and fast-food industry where surplus food and ingredients are often discarded. This rampant food waste not only has a significant environmental impact, but it also overlooks the potential value of these resources that could otherwise be tapped into.  
    Solution: I envision a unique and exciting solution where restaurants and fast-food chains create partnerships with local composting enterprises. In this system, these businesses would collect their food waste and sell it to composting companies who would then convert this waste into nutrient-rich soil. This soil can be sold back to local agricultural producers or to the general public for home gardening use. Not only does this minimize the amount of food waste going into landfills, it creates a new revenue stream for both the restaurants and the composting companies. Moreover, this rotation completes a full-circle economy where resources are put to best use. It promotes healthy eating, community growth and a sense of unity as we all strive for a greener and healthier earth. This action might seem small, but the collective impact can be massive! Let's turn the tide on food waste and create a tastier and greener future together!
    Category: Food waste
    Feasibility Score: 7

    Example 2:
    Problem: The colossal waste produced by the fashion industry is a problem with major environmental implications. The fashion industry is the second largest polluter in the world, and it contributes to significant amounts of waste, with 85% of textiles going to the dump each year. With the rise of fast fashion, clothes are manufactured, purchased, and discarded at an alarming rate. This creates not just waste, but also a tremendous waste of resources, including water, energy, and labor.   
    Solution: The proposed solution is a platform that enables and encourages ""Clothing as a Service"" (CaaS). The goal of the platform is to shift the mindset from owning clothes to accessing them, reminiscent of the boom in car sharing and ride-hailing services, and increasingly music, film, and software products.  The core of this platform is to allow users to lease clothes for a certain period of time after which they can choose to return, swap, or purchase the items - like a library but for clothes. This allows for a rotation of clothes in people's wardrobes and the clothes get reused by multiple users over their lifetime, thereby ensuring maximum usage of every piece. The returned clothes can be refurbished and repaired if necessary, adding to the lifecycle of the clothing.  For businesses, this opens up new revenue streams and provides more insight into consumer habits and preferences, enhancing their ability to tailor offers and products. For consumers, it offers financial savings, variety, and convenience, while positively impacting the environment. With a strong infrastructure for transport, cleaning, repairing, and recycling, and strategic partnerships with fashion brands, this platform can become a scalable and sustainable solution to the waste problem plaguing the fashion industry. The feasibility of implementation lies in changing consumer behavior towards renting instead of buying - a trend already catching on for its environmental and economic benefits.
    Category: Fashion
    Feasibility Score: 8

    Example 3:
    Problem: Spent nuclear fuel can be recycled to make new fuel and byproducts.
    Solution: Nuclear Waste recycling has, to date, mostly been focused on the extraction of plutonium and uranium, as these elements can be reused in conventional reactors. This separated plutonium and uranium can subsequently be mixed with fresh uranium and made into new fuel rods.
    Category: Energy
    Feasibility Score: 5

    Now, assess the following business idea:
    Problem: {problem}
    Solution: {solution}
    Category: {category}
    
    Provide a feasibility score from 1 to 10. You should only return an integer, no words or explanation needed. If there's an error, return "Error".  
    """
    response = get_openai_response(prompt)
    return response

def get_novelty_score(problem, solution, category):
    """
    Generates a prompt for an AI model to output a novelty score from 1 to 10 for a business,
    based on the provided problem, solution, and category. Includes examples for training.
    """
    prompt = f"""
    Evaluate the novelty of business ideas on a scale from 1 to 10, with 10 being highly novel and unique. Use the following examples to guide your scoring:

    Example 1:
    Problem: Many students struggle with affording textbooks each semester due to high costs, contributing to financial stress during their academic studies.  .
    Solution: Implement a textbook rental system within universities so students can lease instead of buying them. This not only makes education more affordable but also promotes reusable resources, driving the educational sector towards a circular economy. The used textbooks can be repaired or refurbished if necessary, ensuring their maximum use. The system could also incorporate a platform for students to share or exchange books, facilitating further reuse.
    Category: Paper and cupboard
    Novelty Score: 3

    Example 2:
    Problem: Single-use packaging, primarily plastic, is contributing to significant environmental pollution and resource waste.  
    Solution: My solution involves creating a robust reusable packaging system for the food and beverage industry. Existing solutions like returnable glass bottles or bags have shown that it's possible and have been embraced by consumers. My proposal expands on this idea by introducing a universal, industry-standard system of reusable packaging for a wider range of products, including takeaway foods, groceries, and beverages.  Consumers would pay a small deposit fee for each reusable package, which would be refunded upon returning the item or used towards their next purchase. Retailers would then clean and sterilize these containers to be used again.   This initiative could be supported by a collaborative scheme involving local businesses, packaging companies, logistics providers, and cleaning services, ensuring the required infrastructure for collection, cleaning, and redistribution of reusable items is in place.  The environmental impact would be immense, drastically reducing the amount of single-use packaging going to landfills or into our oceans. Simultaneously, it generates financial value since businesses can save costs on sourcing new packaging material. Although initial investment on procuring and maintaining the reusable packaging will be required, the long-term savings outweigh these costs.  This is feasible as it builds on mechanisms that are already familiar to consumers and businesses—namely deposit-refund systems. With increased public concern about plastic waste, customer acceptance and preference for reusable packaging options can be expected. Coming to scalability, starting local will be the best approach. Once the pilot is successful, it can be scaled to include more businesses, or even entire cities or states.  
    Category: Packaging 
    Novelty Score: 7

    Example 3:
    Problem: The problem that this idea is meant to address is the large amount of waste generated in the construction industry. In particular, the construction process generates a significant amount of waste from building materials, tools, and equipment. This waste contributes to landfills, pollution, and resource depletion. Additionally, traditional construction practices often result in buildings and structures that are designed for a single use and have a limited lifespan, leading to the frequent demolition and replacement of buildings. This results in the loss of valuable resources, including materials, energy, and labor.
    Solution: The idea is to reduce the waste generated in the construction industry by using modular building components that can be reused and repurposed in different projects. These components would be designed to be easily disassembled, transported, and reassembled, reducing the need for new materials and conserving resources. This is a new and innovative solution that is still in the early stages of development.So, imagine you're building a house and instead of using traditional building materials that will only be used once, you use modular components that can be taken apart and used again on a different project. This not only helps to reduce waste, but also conserves resources and reduces the environmental impact of construction. I believe this idea has the potential to revolutionize the way buildings are constructed and help to create a more circular construction industry
    Category: Construction
    Novelty Score: 7

    Now, assess the following business idea:
    Problem: {problem}
    Solution: {solution}
    Category: {category}
    
    Provide a novelty/uniqueness score from 1 to 10. You should only return an integer, no words or explanation needed. If there's an error, return "Error".  
    """
    response = get_openai_response(prompt)
    return response

def get_env_impact_score(problem, solution, category):
    """
    Generates a prompt for an AI model to assess the environmental impact of a business idea.
    The impact is rated on a scale from 1 to 10, with 10 being the most positive impact.
    Includes examples for training.
    """
    prompt = f"""
    Assess the environmental impact of a business idea. The impact is rated on a scale from 1 to 10, with 10 being the most positive impact.
    Here are examples of business ideas with their environmental and economic impact scores:

    Example 1:
    Problem: A significant issue is the overuse and wastage of paper in office environments. Every year, an estimated 50% of business waste consists of paper, contributing to deforestation and significant CO2 emissions. Additionally, producing paper absorbs a lot of energy and water, and many companies are not efficiently managing their paper use. Many documents are printed out, only to be used temporarily and then discarded, leading to massive waste. The excessive reliance on paper also leads to greater costs for businesses. This culture of paper waste not only harms our environment but also negatively impacts the financial health of businesses.  
    Solution: My solution is a centralized, AI-driven document management system that promotes a paperless culture. This system would handle all digital documents, analyze usage patterns, and encourage digital alternatives to printing. It could incorporate features such as real-time OCR (Optical Character Recognition) for scanning physical documents, collaboration tools, cloud storage, and intelligent searching. It could even recommend when printing is unavoidable and offer solutions such as using recycled paper. This could drastically cut down on paper usage, thereby saving costs, and reduce a company's carbon footprint. Simultaneously, it also offers a chance for a company to increase its operational efficiency by managing and coordinating all its documents in a single, accessible panel.
    Category: Paper and Cupboard
    Environmental Impact Score: 9

    Example 2:
    Problem: The global food system, a major contributor to climate change, is plagued by inefficiencies leading to substantial food waste and greenhouse gas emissions. Urbanization and population growth enhance the urgency to transition to a more sustainable model.  
    Solution: We propose the ""Integrated Digital Platform for Community-Based Circular Food Systems (IDPCB-CFS)"". This platform would link local households, farmers, retailers, and waste treatment facilities, thus forming a circular local food system.  In this system, households, urban farmers, and commercial businesses grow fruits and vegetables using vertical farming and aquaponics, reducing their dependency on long-distance supply chains. The platform provides real-time guidance on optimal planting and harvesting times, and identifies local market needs to minimize overproduction and waste.   Surplus (yield above household consumption or aesthetic noncompliant produce) can be sold or exchanged via the platform, reducing food waste. Deliveries can be bundled and optimized, further reducing transport emissions.  Food waste from households is collected and composted at local organic waste facilities and then distributed back to the participating urban growers as a nutrient-rich natural fertilizer.  Community-based crowdfunding and shared ownership models can reduce the financial barriers to entry. Meanwhile, the use of renewable energy systems (like solar-powered grow lights) can decrease dependence on non-renewable resources, thus adding to the environmental benefits.  IDPCB-CFS faces various practical challenges, like the need for broad community involvement and potential spatial limitations in densely populated areas. However, with the right policies in place and sufficient community buy-in, it promises a viable, scalable, and impactful solution.
    Category: Food Waste
    Environmental Impact Score: 9

    Example 3:
    Problem: Designing Colors schemes
    Solution: Now a days everyone likes white and black color in everything we have. People more likes black and white color for thier car, cloths, equipment, accessories, and many more they have. If people continually use just two colors white and black then in some upcoming years our planet will loss thier beauty. God made this universe colorful and we humans forget all other colors when we have white and black. Even I noticed buildings are also black. I want to ask those people and also from mine why we are using all colors for everything. Please do something for this. Help me to call people kindly just take a look in nature this is colorful and more beautiful than we are making everything in white and black. Our planet is losing it's beautiful color due to us black and white lovers. Everyone, you and me are also involve in this...
    Category: Infrastructure
    Environmental Impact Score: 1

    Based on these examples, assess the following business idea:
    Problem: {problem}
    Solution: {solution}
    Category: {category}
    
    Provide an environmental impact score from 1 to 10. You should only return an integer, no words or explanation needed. If there's an error, return "Error".  
    """

    response = get_openai_response(prompt)
    return response

def get_all_scores(problem, solution, category):
    feasibility_score = get_feasibility_score(problem, solution, category)
    novelty_score = get_novelty_score(problem, solution, category)
    env_impact_score = get_env_impact_score(problem, solution, category)

    if re.search("[0-9]", feasibility_score) == None:
        feasibility_score = "0"
    if re.search("[0-9]", novelty_score) == None:
        novelty_score = "0"
    if re.search("[0-9]", env_impact_score) == None:
        env_impact_score = "0"
        
    overall_score = str(int(re.search("[0-9]",feasibility_score).group()) + 
                        int(re.search("[0-9]",novelty_score).group()) + 
                        int(re.search("[0-9]",env_impact_score).group()))

    # Create a dictionary to hold the scores
    scores_dict = {
        'feasibility_score': feasibility_score,
        'novelty_score': novelty_score,
        'env_impact_score': env_impact_score,
        'overall_score': overall_score
    }

    # Return the dictionary
    return scores_dict

# ---------------------------------------------------------------------
# TOPIC MODELING & INTERPRETATION

dataset = "dataset.csv"
topic_labels = ""

# TODO: Remove
def strip_user_input(user_input):
    # Strip user input to get problem and solution
    # Or get the API to be able to do this
    parts = user_input.split("problem")
    problem_part = parts[1].split("solution")
    user_problem = problem_part[0].strip()
    user_solution = problem_part[1].strip() if len(problem_part) > 1 else ""
    return user_problem, user_solution
    
#user_problem = "Sample problem text"
#user_solution = "Sample solution text"

def get_interpret_prompt():
    """
    Interpret the set of generic topics using trained LDA model output.
    """
    # Read the LDA topics into a string
    # lda_output_string = run_lda_training(dataset)
    with open("lda_topics_dist.txt", 'r') as file:
        lda_topics_dist = file.read()
    
    custom_interpret_instructions = """
    Please provide a brief interpretation of the topics based on this trained LDA model output. Each individual topic should clearly identify a distinct domain or industry. Together, the topics should comprehensively cover the concept of the circular economy, which focuses on reusing and recycling resources to minimize waste. Your interpretation of the topics will be used to classify new problem and solution pairs to the most descriptive and accurate ability. Keep in mind that is the option to classify as "Other" if there is no one topic is sufficient. Format your response as separate lines of Topic X: Name. 

    Here is an example. Given the following,

    Topic 1: 0.031*"food" + 0.009*"business" + 0.008*"system" + 0.007*"local" + 0.007*"container" + 0.007*"community" + 0.006*"material" + 0.006*"product" + 0.006*"recycling" + 0.005*"space"
    Topic 2: 0.018*"model" + 0.012*"fashion" + 0.011*"product" + 0.010*"consumer" + 0.010*"new" + 0.010*"industry" + 0.009*"material" + 0.009*"resource" + 0.009*"recycling" + 0.008*"business"
    Topic 3: 0.013*"paper" + 0.010*"energy" + 0.008*"product" + 0.008*"carbon" + 0.006*"process" + 0.006*"emission" + 0.006*"material" + 0.005*"need" + 0.005*"reduce" + 0.005*"environment"
    Topic 4: 0.034*"plastic" + 0.026*"packaging" + 0.009*"product" + 0.008*"system" + 0.008*"business" + 0.008*"material" + 0.007*"use" + 0.007*"recycling" + 0.006*"singleuse" + 0.006*"container"
    Topic 5: 0.019*"energy" + 0.011*"resource" + 0.010*"system" + 0.010*"use" + 0.008*"sustainable" + 0.007*"product" + 0.007*"business" + 0.006*"reduce" + 0.006*"company" + 0.005*"vehicle"
    Topic 6: 0.018*"material" + 0.011*"construction" + 0.010*"industry" + 0.007*"new" + 0.006*"cost" + 0.006*"resource" + 0.006*"building" + 0.006*"use" + 0.005*"process" + 0.005*"need"

    The topics that were interpreted by a successfully trained model were:
    Topic 1: Food and Agriculture Systems
    Topic 2: Fashion and Consumer
    Topic 3: Energy and Emissions
    Topic 4: Packaging and Single-Use Materials
    Topic 5: Resource Management
    Topic 6: Infrastructure and Construction
    """
    return lda_topics_dist + "\n" + custom_interpret_instructions

def save_interpreted_topics(): 
    interpret_prompt = get_interpret_prompt()
    topic_labels = get_openai_response(interpret_prompt)

    # Write the most up-to-date interpreted topics to a file
    with open('lda_topics.txt', 'w') as f:
        f.write(topic_labels)

def get_interpreted_topics():
    """
    Read the interpreted LDA topics into a string which will be used to 
    augment all evaluation prompts for a circular economy idea.

    TODO: More validation tests
    """
    with open("lda_topics.txt", 'r') as file:
        topic_labels = file.read()
    return f"According to your most recent knowledge, the possible topic labels for classification are: '{topic_labels}'. The format of each topic label is Topic ID: Topic Name."

def predict_category(problem, solution, topic_labels_recall): 
    """
    Classify new user input into one of the interpreted topic labels.
    """
    predict_topic_prompt = f"""
    An individual has submitted a circular economy business idea.

    Problem: '{problem}'
    Solution: '{solution}'

    '{topic_labels_recall}'

    Predict the relevant topic of the new idea. Respond only with the most likely Topic Name. Do not include any numbers or colons. If you are not confident that any topic is appropriate, respond only with the word Other.
    """

    category = get_openai_response(predict_topic_prompt)
    return category

def get_predicted_category(problem, solution): 
    """
    Get the predicted topic of an input idea so that future evaluation
    and scoring can be augmented with this context.
    """
    # Use existing database to get interpreted topics
    save_interpreted_topics()
    topic_labels_recall = get_interpreted_topics()

    # Predict category based on user-submitted problem and solution
    category = predict_category(problem, solution, topic_labels_recall)
    return category
