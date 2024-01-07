from flask import Flask, request, jsonify
from pymongo import MongoClient
#import chat
#from chat import get_openai_response
import chat_fe
from chat_fe import get_openai_response

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

@app.route('/api/get_openai_response', methods=['POST'])
def handle_openai_request():
    print("entered flask")
    user_input = request.json.get('user_input')
    if user_input is not None:
        openai_response = get_openai_response(user_input)
        return jsonify(openai_response)
    else:
        return jsonify({'error': 'Invalid request'}), 400

app.run()