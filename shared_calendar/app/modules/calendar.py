from flask import jsonify
from datetime import datetime
from bson.objectid import ObjectId
from modules.util.fetch_user import *
from modules.util.fetch_calendar import *

def calendar(db, request):
    # Retrieve data from the request JSON
    data_db = request.json  

    # Check user status and retrieve user_id and admin status
    user_id, admin = fetch_user(db, data_db['email'])    

    # Check calendar status and retrieve calendar_id and user_owner status
    calendar_id, user_owner = fetch_calendar(db, data_db['calendar_name'], user_id)

    # If user doesn't exist, return an error
    if not user_id:
        return {"error" : "user_not_found"}

    # If calendar already exists and it's a POST request, return an error
    if calendar_id and request.method == 'POST':
        return {"error" : "calendar_found"}

    try:
        collection = db["calendar"]

        # Handle inserting calendar
        if request.method == 'POST':
            data_db.update({"user_id" : user_id})
            data_db['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            collection.insert_one(data_db)
            return {"calendar_insert" : True}
        
        # Handle getting calendar
        elif request.method == 'GET':
            response = collection.find_one({"_id": ObjectId(calendar_id)})
            response['_id'] = str(response['_id'])
            response['user_id'] = str(response['user_id'])
            return jsonify(response)

        # Handle calendar update
        elif request.method == 'PUT':
            # If user is the owner or an admin, update the calendar document
            if user_owner or admin:
                collection.update_one({"_id": ObjectId(calendar_id)}, {"$set": data_db})
                return {"calendar_update" : True}
            else:
                return {"calendar_update_owner" : False}
        
        # Handle calendar deletion
        elif request.method == 'DELETE':
            # If user is the owner or an admin, delete the calendar document
            if user_owner or admin:
                collection.delete_one({"_id": ObjectId(calendar_id)})
                return {"calendar_delete" : True}
            else:
                return {"calendar_delete_owner" : False}
            
        # Handle unknown methods
        else:
            return {"error" : f"calendar_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_calendar_module"}