from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
from modules.util.fetch_user import *

# Function to handle user operations
def user(db, request):
    # Retrieve data from the request JSON
    data_db = request.json

    # Check user status and retrieve user_id and admin status
    user_id, admin =  fetch_user(db, data_db['email'])

    # If user already exists and it's a POST request, return an error
    if user_id and request.method == 'POST':
        return {"error" : "user_found"}
    
    try:
        collection = db["users"]

        # Handle inserting user
        if request.method == 'POST':
            # Add creation_date to the data
            data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            # Insert the user data into the database
            collection.insert_one(data_db)
            return {"user_insert" : True}
        
        # Handle getting user
        elif request.method == 'GET':
            response = collection.find_one({"_id": ObjectId(user_id)})
            response['_id'] = str(response['_id'])
            return jsonify(response)
            
        # Handle user update
        elif request.method == 'PUT':
            collection.update_one({"_id": ObjectId(user_id)}, {"$set": data_db})
            return {"user_update" : True}

        # Handle user deletion
        elif request.method == 'DELETE':
            collection.delete_one({"_id": ObjectId(user_id)})
            return {"user_delete" : True}

        # Handle unknown methods
        else:
            return {"error" : f"users_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_users_module"}