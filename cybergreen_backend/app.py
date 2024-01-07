from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from chat import get_predicted_category, get_all_scores
from chat import get_base_eval, get_impact_eval, get_risks_eval, get_market_eval, get_regulation_eval, get_competition_eval, get_feasibility_eval, get_funding_eval
from chat_fe import get_openai_response
import os
import sys
import random
from dotenv import load_dotenv
from bson.json_util import dumps

load_dotenv()
mongo_url = os.getenv("MONGO_LINK")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CORS(app, supports_credentials=True)

try:
  client = MongoClient(mongo_url)
  
# return a friendly error if a URI error is thrown 
except errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
  
db = client.flask_db
submissions = db.submissions

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/chat")
def test_chat(user_input):
    return get_openai_response(user_input)

# ---------------------------------------------------------------------
# HELPER FUNCTIONS - IDEA EVALUATION & SCORING

def eval_idea(problem, solution):
    category = get_predicted_category(problem, solution)
    base_eval = get_base_eval(problem, solution, category)
    return base_eval

def score_idea(problem, solution):
    category = get_predicted_category(problem, solution)
    scores = get_all_scores(problem, solution, category)
    return scores

def get_base_response(problem, solution):
    """
    Return the formatted string with base evaluation and scores.
    """
    base_eval = eval_idea(problem, solution)
    scores = score_idea(problem, solution)

    # Access individual scores
    feasibility_score = scores['feasibility_score']
    novelty_score = scores['novelty_score']
    env_impact_score = scores['env_impact_score']
    overall_score = scores['overall_score']

    # Create a formatted string with the scores (auto-converts integers)
    scores_string = (
        f"Feasibility: {feasibility_score}. "
        f"Novelty: {novelty_score}. "
        f"Environmental Impact: {env_impact_score}. "
        f"Overall: {overall_score}."
    )

    return base_eval + " " + scores_string

# ---------------------------------------------------------------------
# LIVE ROUTES

@app.route("/submission", methods=("GET", "POST", "OPTIONS"))
def submission():
    print("hi")
    if request.method=="POST":
        # Submit the submission
        user_input = request.json
        print(user_input)
        for input in user_input:
            # Retrieve problem, solution from a single input
            problem = input["problem"]
            solution = input["solution"]

            # Save predicted category to db
            category = get_predicted_category(problem, solution)
            input["category"] = category

            # Save scores to db
            scores = get_all_scores(problem, solution, category)        

            feasibility_score = scores['feasibility_score']
            novelty_score = scores['novelty_score']
            env_impact_score = scores['env_impact_score']
            overall_score = scores['overall_score']

            input["feasibility_score"] = feasibility_score
            input["novelty_score"] = novelty_score
            input["env_impact_score"] = env_impact_score
            input["overall_score"] = overall_score
        
        submissions.insert_many(user_input)
                
        return jsonify({
            "response": scores, 
            "Access-Control-Allow-Origin": "*",
        })
    all_submissions = submissions.find()
    return jsonify({"response": dumps(all_submissions), "Access-Control-Allow-Origin": "*"})

@app.route("/user_chat", methods=['GET', 'POST'])
def chat():
    """
    As soon as the user submits their idea, the system predicts
    the idea's category and scores the idea within that category.
    This is used to generate and return a base evaluation response with
    all scores. 
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    
    # user_input = "Problem: " + problem + " Solution: " + solution
    if not problem or not solution:
        return jsonify({"error": "Missing user_input parameter(s)."})
    
    # Predict category based on problem and solution
    category = get_predicted_category(problem, solution)

    # Get generated base evaluation response 
    string_res = get_base_response(problem, solution)
    response = {
        'str': string_res,
        'category': category
    }

    return jsonify({"response": response, "Access-Control-Allow-Origin": "*"})

# ---------------------------------------------------------------------
# FOLLOW-UP EVALUATIONS

@app.route("/impact", methods=['POST'])
def eval_impact():
    """
    Endpoint for additional evaluation when the user clicks the "Comprehensive Impact" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform impact evaluation
    impact_eval = get_impact_eval(problem, solution, category)

    return jsonify({"response": impact_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/risks", methods=['POST'])
def eval_risks():
    """
    Endpoint for additional evaluation when the user clicks the "Business and Financial Risks" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform risks evaluation
    risks_eval = get_risks_eval(problem, solution, category)

    return jsonify({"response": risks_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/market", methods=['POST'])
def eval_market():
    """
    Endpoint for additional evaluation when the user clicks the "Market Insights and Outlooks" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform market evaluation
    market_eval = get_market_eval(problem, solution, category)

    return jsonify({"response": market_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/regulation", methods=['POST'])
def eval_regulation():
    """
    Endpoint for additional evaluation when the user clicks the "Regulation and Compliance" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform regulation evaluation
    regulation_eval = get_regulation_eval(problem, solution, category)

    return jsonify({"response": regulation_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/competition", methods=['POST'])
def eval_competition():
    """
    Endpoint for additional evaluation when the user clicks the "Competitive Advantage" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform competition evaluation
    competition_eval = get_competition_eval(problem, solution, category)

    return jsonify({"response": competition_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/feasibility", methods=['POST'])
def eval_feasibility():
    """
    Endpoint for additional evaluation when the user clicks the "Idea and Concept Feasibility" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform feasibility evaluation
    feasibility_eval = get_feasibility_eval(problem, solution, category)

    return jsonify({"response": feasibility_eval, "Access-Control-Allow-Origin": "*"})

@app.route("/funding", methods=['POST'])
def eval_risks():
    """
    Endpoint for additional evaluation when the user clicks the "Potential Funding Outlook" button.
    """
    # Get user query params from JSON data
    problem = request.json['problem']
    solution = request.json['solution']
    category = request.json['category']

    if not problem or not solution or not category:
        return jsonify({"error": "Missing 'problem', 'solution', or 'category'."})

    # Perform funding evaluation
    funding_eval = get_funding_eval(problem, solution, category)

    return jsonify({"response": funding_eval, "Access-Control-Allow-Origin": "*"})

# ---------------------------------------------------------------------
# CSV FILE

@app.route('/process_csv', methods=['POST', 'OPTIONS'])
def process_csv():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        data = request.json
        # Perform actions with each pair of problem and solution
        for row in data:
            problem = row['problem']
            solution = row['solution']
            # Perform your custom logic with problem and solution here
            print(f"Problem: {problem}, Solution: {solution}")

        # Do not set Access-Control-Allow-Origin to '*' in the actual response
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

app.run()