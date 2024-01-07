import chat
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
mongo_url = os.getenv("MONGO_LINK")

client = MongoClient('localhost', 27017)
db = client.flask_db
submissions = db.submissions

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/submissions", methods=("GET", "POST"))
def submissions():
    if request.method=="POST":
        # Submit the submission
        problem = request.form['problem']
        solution = request.form['solution']
        overall_score = request.form['overall_score']
        topic = request.form['topic']
        return jsonify(success=True)
    all_submissions = submissions.find()
    return jsonify(success=True)

@app.route("/chat")
def test_chat(user_input):
    return get_openai_response(user_input)

app.run()