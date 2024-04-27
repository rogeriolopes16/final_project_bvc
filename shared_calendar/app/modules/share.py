from flask import jsonify
from bson.objectid import ObjectId
from datetime import datetime
from modules.util.fetch_user import *
from modules.util.fetch_calendar import *
from modules.util.fetch_group import *
from modules.util.fetch_group import *

# Function to handle share operations
def share(db, request):
    # Retrieve data from the request JSON
    data_db = request.json  

    # Check user status and retrieve user_id and admin status
    user_id, admin = fetch_user(db, data_db['email'])

    # Check calendar status and retrieve calendar_id and user_owner status
    calendar_id, user_owner = fetch_calendar(db, data_db['calendar_name'], user_id)

    # Check group status and retrieve group_id and share_list
    group_id, share_list = fetch_group(db, data_db['group_name'])
       
    # If group doesn't exist, return an error
    if not group_id:
        return {"error" : "group_not_found"}
    
    # If user doesn't exist, return an error    
    if not user_id:
        return {"error" : "user_not_found"}

    # If calendar doesn't exist, return an error
    if not calendar_id:
        return {"error" : "calendar_not_found"}

    try:
        collection = db["group"]

        # Handle updating share list
        if request.method in ['POST','PUT']:
            # Check if the user is the owner or an admin
            if user_owner or admin:
                # Iterate over each email in the share list
                for email in data_db['share']:
                    # Check if the user with the email exists
                    if fetch_user(db, email)[0]:
                        # If user exists, add their user_id to the share_list
                        share_list.append(str(fetch_user(db, email)[0]))
                # Update the share list in the group document
                collection.update_one({"_id": ObjectId(group_id)}, {"$set": {"share": list(set(share_list))}})
                return {"share_update" : True}
            else:
                return {"share_update_owner" : False}
   
        # Handle getting shared users
        elif request.method == 'GET':
            share_dict = {}
            collection = db["users"]
            # Iterate over each user_id in the share_list
            for share_user in share_list:
                response = collection.find_one({"_id": ObjectId(share_user)})
                response['_id'] = str(response['_id'])
                share_dict.update({f"{response['_id']}" : response})
            return jsonify(share_dict)
            
        # Handle removing users from share list
        elif request.method == 'DELETE':
            # Check if the user is the owner or an admin
            if user_owner or admin:
                # Iterate over each email in the share list
                for email in data_db['share']:
                    user_id = str(fetch_user(db, email)[0])
                    # If user_id is in the share_list, remove it
                    if user_id in share_list:
                        share_list.remove(user_id)
                # Update the share list in the group document
                collection.update_one({"_id": ObjectId(group_id)}, {"$set": {"share": list(set(share_list))}})
                return {"share_delete" : True}
            else:
                return {"share_delete_owner" : False}
            
        # Handle unknown methods
        else:
            return {"error" : f"share_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_share_module"}