from flask import Flask, jsonify, request
from pymongo import MongoClient
from modules.budget import *
from modules.budget_category import *
from modules.budget_category_type import *
from modules.budget_project_type import *
from modules.budget_group import *
from modules.budget_operation import *

# Initialize Flask app
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["calendar_db"]

# Endpoint for budget operations
@app.route('/budget', methods=['POST', 'GET', 'PUT', 'DELETE'])
def budget_():
    return budget(db, request)

# Endpoint for expense operations
@app.route('/budget/expense', methods=['POST', 'PUT', 'DELETE'])
def expense_():
    return budget_operation(db, request, 'expense')

# Endpoint for revenue operations
@app.route('/budget/revenue', methods=['POST', 'PUT', 'DELETE'])
def revenue_():
    return budget_operation(db, request, 'revenue')

# Endpoint for budget_category operations
@app.route('/budget_category', methods=['POST', 'GET', 'PUT', 'DELETE'])
def budget_category_():
    return budget_category(db, request)

# Endpoint for budget_category_type operations
@app.route('/budget_category_type', methods=['POST', 'GET', 'PUT', 'DELETE'])
def budget_category_type_():
    return budget_category_type(db, request)

# Endpoint for budget_project_type operations
@app.route('/budget_project_type', methods=['POST', 'GET', 'PUT', 'DELETE'])
def budget_project_type_():
    return budget_project_type(db, request)

# Endpoint for budget_group operations
@app.route('/budget_group', methods=['POST', 'GET', 'PUT', 'DELETE'])
def budget_group_():
    return budget_group(db, request)

if __name__ == '__main__':
    # Run the Flask app
    print("Budget API")
    app.run(debug=True, host='0.0.0.0', port=3000)

