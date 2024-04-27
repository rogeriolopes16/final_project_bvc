from flask import jsonify
from bson.objectid import ObjectId
from datetime import datetime
from modules.util.fetch_user import *
from modules.util.fetch_calendar import *
from modules.util.fetch_event import *

# Function to handle event operations
def attendance(db, request):
    # Retrieve data from the request JSON
    data_db = request.json  

    # Check event status and retrieve event_id
    event_id = fetch_event(db, data_db['event_name'])

    # If event already exists and it's a POST request, return an error
    if event_id and request.method == 'POST':
        return {"error" : "event_found"}

    try:
        collection = db["event"]
            
        # Handle event update
        if request.method == 'PUT':
            response = collection.find_one({"_id": ObjectId(event_id)})
            for line in response['attendance']:
                if line[0] == data_db['attendance'][0]:
                    line[1] = data_db['attendance'][1]
            collection.update_one({"_id": ObjectId(event_id)}, {"$set": response})
            return {"attendance_update" : True}
        # Handle unknown methods
        else:
            return {"error" : f"attendance_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_attendance_module"}