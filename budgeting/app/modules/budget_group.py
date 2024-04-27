from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
from modules.util.fetch_user import *
import json

# Function to handle budget operations
def budget_group(db, request):
    
    # Retrieve data from the request JSON
    data_db = request.json

    try:
        collection = db["budget_group"]

        # Handle inserting budget_group
        if request.method == 'POST':
            # Add creation_date to the data
            data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            # Insert the budget_group data into the database
            collection.insert_one(data_db)
            return {"budget_group_insert" : True}
        
        # Handle getting budget_group
        elif request.method == 'GET':
            response = collection.find()
            response_list = []
            for result in list(response):
                result['_id'] = str(result['_id'])
                response_list.append(result)
            response = response_list
            return jsonify(response)
            
        # Handle budget_group update
        elif request.method == 'PUT':
            document_id = data_db['_id']
            del data_db['_id']
            collection.update_one({"_id": ObjectId(document_id)}, {"$set": data_db})
            return {"budget_group_update" : True}

        # Handle budget_group deletion
        elif request.method == 'DELETE':
            collection.delete_one({"_id": ObjectId(data_db['_id'])})
            return {"budget_group_delete" : True}

        # Handle unknown methods
        else:
            return {"error" : f"budget_group_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_budget_group_module"}