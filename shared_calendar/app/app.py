from flask import Flask, jsonify, request
from pymongo import MongoClient
from modules.calendar import *
from modules.user import *
from modules.event import *
from modules.group import *
from modules.share import *
from modules.attendance import *

# Initialize Flask app
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["calendar_db"]

# Endpoint for user operations
@app.route('/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
def users_():
    return user(db, request)

# Endpoint for calendar operations
@app.route('/calendar', methods=['POST', 'GET', 'PUT', 'DELETE'])
def calendar_():
    return calendar(db, request)

# Endpoint for event operations
@app.route('/event', methods=['POST', 'GET', 'PUT', 'DELETE'])
def event_():
    return event(db, request)

# Endpoint for group operations
@app.route('/group', methods=['POST', 'GET', 'PUT', 'DELETE'])
def group_():
    return group(db, request)

# Endpoint for sharing operations
@app.route('/share', methods=['POST', 'GET', 'PUT', 'DELETE'])
def share_():
    return share(db, request)

# Endpoint for attendance operations
@app.route('/attendance', methods=['PUT'])
def attendance_():
    return attendance(db, request)

if __name__ == '__main__':
    # Run the Flask app
    print("Calendar API")
    app.run(debug=True, host='0.0.0.0', port=3000)

