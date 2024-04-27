from flask import Flask, jsonify, request
from pymongo import MongoClient
from modules.vote import *

# Initialize Flask app
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["calendar_db"]

# Endpoint for create_poll operations
@app.route('/create_poll', methods=['POST'])
def create_poll_():
    return create_poll(db, request)

# Endpoint for vote operations
@app.route('/vote', methods=['POST'])
def vote_():
    return vote(db, request)

# Endpoint for get vote operations
@app.route('/get_results_polls')
def get_results_polls_():
    return get_results_polls(db, request)

if __name__ == '__main__':
    # Run the Flask app
    print("Vote API")
    app.run(debug=True, host='0.0.0.0', port=3000)

