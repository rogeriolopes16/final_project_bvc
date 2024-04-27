from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
from modules.util.fetch_user import *
import json

# Function to handle budget operations
def budget_category_type(db, request):
    
    # Retrieve data from the request JSON
    data_db = request.json

    try:
        collection = db["budget_category_type"]

        # Handle inserting budget_category_type
        if request.method == 'POST':
            if data_db['budget_id']:
                # Add creation_date to the data
                data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                # Add budget_id 
                data_db["budget_id"] = ObjectId(data_db['budget_id'])
                # Insert the budget_category_type data into the database
                collection.insert_one(data_db)
                return {"budget_category_type_insert" : True}
            else:
                return {"budget_id" : "required"}
        
        # Handle getting budget_category_type
        elif request.method == 'GET':
            response = collection.find({"budget_id": ObjectId(data_db['budget_id'])})
            response_list = []
            for result in list(response):
                result['_id'] = str(result['_id'])
                result['budget_id'] = str(result['budget_id'])
                response_list.append(result)
            response = response_list
            return jsonify(response)
            
        # Handle budget_category_type update
        elif request.method == 'PUT':
            document_id = data_db['_id']
            del data_db['_id']
            collection.update_one({"_id": ObjectId(document_id)}, {"$set": data_db})
            return {"budget_category_type_update" : True}

        # Handle budget_category_type deletion
        elif request.method == 'DELETE':
            collection.delete_one({"_id": ObjectId(data_db['_id'])})
            return {"budget_category_type_delete" : True}

        # Handle unknown methods
        else:
            return {"error" : f"budget_category_type_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_budget_category_type_module"}