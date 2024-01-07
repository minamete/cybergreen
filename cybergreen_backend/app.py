from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from chat_fe import get_openai_response
from chat_idea import eval_idea

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client.flask_db
submissions = db.submissions

@app.route("/submission", methods=("GET", "POST", "OPTIONS"))
def submission():
    print("hi")
    if request.method=="POST":
        # Submit the submission
        user_input = request.args.get('submit')
        problem = user_input[0]
        solution = user_input[1]
        score = user_input[2]
         
        # Run through score
        # topic = request.args.get('topic')
        
        
        return jsonify({
            "response": "Submission successful", 
            "Access-Control-Allow-Origin": "*",
        })
    all_submissions = submissions.find()
    return jsonify({"response": "abc", "Access-Control-Allow-Origin": "*"})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/chat")
def test_chat(user_input):
    return get_openai_response(user_input)

@app.route("/user_chat", methods=['GET', 'POST'])
def chat():
    # user_input = request.args.get('user_input')  # Get user input from query parameters
    # if user_input is None:
    #     return "Error: user_input parameter is missing."

    # # Call the get_openai_response function
    # response = get_openai_response(user_input)
    # return jsonify({"response": response, "Access-Control-Allow-Origin": "*"})
    
    user_input = request.args.get('user_input')  # Get user input from query parameters
    if user_input is None:
        return jsonify({"error": "user_input parameter is missing."}), 400
    
    # Do additional processing with user_problem and user_solution
    user_problem = request.args.get('user_problem')
    user_solution = request.args.get('user_solution')

    response = eval_idea(user_problem, user_solution)
    return jsonify({"response": response, "Access-Control-Allow-Origin": "*"})

app.run()