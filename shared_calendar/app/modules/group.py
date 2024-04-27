from flask import jsonify
from bson.objectid import ObjectId
from datetime import datetime
from modules.util.fetch_user import *
from modules.util.fetch_calendar import *
from modules.util.fetch_group import *
from modules.util.fetch_group import *

# Function to handle group operations
def group(db, request):
    # Retrieve data from the request JSON
    data_db = request.json  

    # Check user status and retrieve user_id and admin status
    user_id, admin = fetch_user(db, data_db['email'])

    # Check calendar status and retrieve calendar_id and user_owner status
    calendar_id, user_owner = fetch_calendar(db, data_db['calendar_name'], user_id)

    # Check group status and retrieve group_id
    group_id = fetch_group(db, data_db['group_name'])
       
    # If group already exists and it's a POST request, return an error
    if group_id and request.method == 'POST':
        return {"error" : "group_found"}

    # If user doesn't exist, return an error
    if not user_id:
        return {"error" : "user_not_found"}

    # If calendar doesn't exist, return an error
    if not calendar_id:
        return {"error" : "calendar_not_found"}

    try:
        collection = db["group"]

        # Handle inserting group
        if request.method == 'POST':
            data_db.update({"user_id" : user_id, "calendar_id" : calendar_id})
            data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            collection.insert_one(data_db)
            return {"group_insert" : True}
   
        # Handle getting group
        elif request.method == 'GET':
            response = collection.find_one({"_id": ObjectId(group_id)})
            response['_id'] = str(response['_id'])
            response['user_id'] = str(response['user_id'])
            response['calendar_id'] = str(response['calendar_id'])
            return jsonify(response)

        # Handle group update
        elif request.method == 'PUT':
            # If user is the owner or an admin, update the group document
            if user_owner or admin:
                collection.update_one({"_id": ObjectId(group_id)}, {"$set": data_db})
                return {"group_update" : True}
            else:
                return {"group_update_owner" : False}
            
        # Handle group deletion
        elif request.method == 'DELETE':
            # If user is the owner or an admin, delete the group document
            if user_owner or admin:
                collection.delete_one({"_id": ObjectId(group_id)})
                return {"group_delete" : True}
            else:
                return {"group_delete_owner" : False}
            
        # Handle unknown methods
        else:
            return {"error" : f"group_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_group_module"}