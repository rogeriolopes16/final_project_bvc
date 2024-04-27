from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
from modules.util.fetch_user import *
import json

# Function to handle budget operations
def budget(db, request):
    
    # Retrieve data from the request JSON
    data_db = request.json

    try:
        collection = db["budget"]

        # Handle inserting budget
        if request.method == 'POST':
            # Add creation_date to the data
            data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            # Add balance to the data
            data_db['balance'] = 0.0
            # Add budget_project_type name
            data_db['budget_project_type_name'] = db["budget_project_type"].find_one({"_id": ObjectId(data_db['budget_project_type'])})['name']
            # Add budget_group name
            data_db['budget_group_name'] = db["budget_group"].find_one({"_id": ObjectId(data_db['budget_group'])})['name']
            # Add blank dicts
            data_db['expenses'], data_db['revenue'] = {}, {}
            # Insert the budget data into the database
            collection.insert_one(data_db)
            return {"budget_insert" : True}
        
        # Handle getting budget
        elif request.method == 'GET':
            if data_db['budget_get'] == 'unique':
                response = collection.find_one({"_id": ObjectId(data_db['_id']), "email": data_db['email']})
                response['_id'] = str(response['_id'])
            elif data_db['budget_get'] == 'all':
                response = collection.find({"email": data_db['email']})
                response_list = []
                for result in list(response):
                    result['_id'] = str(result['_id'])
                    response_list.append(result)
                response = response_list
            return jsonify(response)
            
        # Handle budget update
        elif request.method == 'PUT':
            collection.update_one({"$and": [{"_id": ObjectId(data_db['_id'])}, {"email": data_db['email']}]}, {"$set": data_db})
            return {"budget_update" : True}

        # Handle budget deletion
        elif request.method == 'DELETE':
            collection.delete_one({"$and": [{"_id": ObjectId(data_db['_id']), "email": data_db['email']}]})
            return {"budget_delete" : True}

        # Handle unknown methods
        else:
            return {"error" : f"budget_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_budget_module"}