import chat
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_db
submissions = db.submissions

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/chat")
def test_chat(user_input):
    return get_openai_response(user_input)

app.run()