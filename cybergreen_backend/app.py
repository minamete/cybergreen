from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from chat_fe import get_openai_response

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client.flask_db
submissions = db.submissions

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/chat")
def test_chat(user_input):
    return get_openai_response(user_input)

@app.route("/user_chat")
def chat():
    user_input = request.args.get('user_input')  # Get user input from query parameters
    if user_input is None:
        return "Error: user_input parameter is missing."

    # Call the get_openai_response function
    response = get_openai_response(user_input)
    return jsonify({"response": response})


app.run()