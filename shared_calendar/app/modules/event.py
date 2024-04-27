from flask import jsonify
from bson.objectid import ObjectId
from datetime import datetime, timedelta, timezone
from modules.util.date_time import date_time_
from modules.util.fetch_user import *
from modules.util.fetch_calendar import *
from modules.util.fetch_event import *
import copy
import pytz

# Function to handle event operations
def event(db, request):
    # Retrieve data from the request JSON
    data_db = request.json  

    # Check user status and retrieve user_id and admin status
    user_id, admin = fetch_user(db, data_db['email'])

    # Check calendar status and retrieve calendar_id and user_owner status
    calendar_id, user_owner = fetch_calendar(db, data_db['calendar_name'], user_id)

    # Check event status and retrieve event_id
    event_id = fetch_event(db, data_db['event_name'], data_db["start_date_time"])

    # If event already exists and it's a POST request, return an error
    if event_id and request.method == 'POST':
        return {"error" : "event_found"}

    # If user doesn't exist, return an error
    if not user_id:
        return {"error" : "user_not_found"}

    # If calendar doesn't exist, return an error    
    if not calendar_id:
        return {"error" : "calendar_not_found"}

    try:
        collection = db["event"]

        # Handle inserting event
        if request.method == 'POST':
            creation_date_time = datetime.now().strftime('%Y-%m-%d_%H:%M')
            event_start_date_time = date_time_(data_db['start_date_time'])
            event_end_date_time = date_time_(data_db['end_date_time'])

            data_db.update({"user_id" : user_id, "calendar_id" : calendar_id})
            data_db['start_date_time'] = event_start_date_time
            data_db['end_date_time'] = event_end_date_time
            data_db['creation_date_time'] = creation_date_time

            # Create series id using last five characters of user_id + event creation_time
            series_id = str(user_id)[-5:] +"_"+ str(datetime.now().timestamp()).replace('.','')
            # Series_id is equal for all events on the same series
            data_db['series_id'] = series_id

            # Handle event repetition
            if data_db['repeats'] and data_db['repeats'] != 'no':
               
                end_repetition_date = date_time_(data_db['until'])

                match data_db['repeats']:
                    case "daily": repetition_delta = {"days": 1}
                    case "weekly": repetition_delta = {"days": 7}
                    case "monthly_day": repetition_delta = {"months": 1}
                    case _: repetition_delta = {"years": 9999}
                    # TODO add case for monthly_weekday (ex: second Sunday of the month)

                # Print series creation attempt:
                print(f"[{user_id}] Creating event series {data_db['event_name']} \nFirst: {str(event_start_date_time)[:-3]} - {str(event_end_date_time)[:-3]} ...")
                
                while event_start_date_time <= end_repetition_date:
                    if event_end_date_time > event_start_date_time:
                        try:
                            # Create a shallow copy of data_db
                            data_db_copy = copy.copy(data_db)
                            collection.insert_one(data_db_copy)
                            event_start_date_time += timedelta(**repetition_delta)
                            event_end_date_time += timedelta(**repetition_delta)
                            
                            # Update the start and end dates in the copied dictionary
                            data_db['start_date_time'] = event_start_date_time
                            data_db['end_date_time'] = event_end_date_time
                            
                        except Exception as e:
                            print(e)
                            return {"error" : "except_event_module: could not create series"}  
                          
                # Print series creation confirmation:
                print(f"Last:  {str(event_start_date_time)[:-3]} - {str(event_end_date_time)[:-3]} - Success.")
                        
                return {"event_insert_series" : True}    
            
            elif event_end_date_time > event_start_date_time:
                #Print event confirmation
                print(f"[{user_id}] Created event {data_db['event_name']}:\n{str(event_start_date_time)[:-3]} - {str(event_end_date_time)[:-3]}. Success.")
                collection.insert_one(data_db)
                return {"event_insert" : True}
            else:
                print(f"[{user_id}] event {data_db['event_name']}:\n{str(event_start_date_time)[:-3]} - {str(event_end_date_time)[:-3]}. FAIL.")
                return {"error" : "Start date must be before end date"}
            
        # Handle getting event
        elif request.method == 'GET':
            response = collection.find_one({"_id": ObjectId(event_id)})
            response['_id'] = str(response['_id'])
            response['user_id'] = str(response['user_id'])
            response['calendar_id'] = str(response['calendar_id'])
            return jsonify(response)

        # Handle event update
        elif request.method == 'PUT':
            # If user is the owner or an admin, update the event document
            if user_owner or admin:
                collection.update_one({"_id": ObjectId(event_id)}, {"$set": data_db})
                return {"event_update" : True}
            else:
                return {"event_update_owner" : False}
            
        # Handle event deletion
        elif request.method == 'DELETE':
            # If user is the owner or an admin, delete the event document
            if user_owner or admin:
                collection.delete_many({'series_id': series_id})
                return {"event_delete" : True}
            else:
                return {"event_delete_owner" : False}
            
        # Handle unknown methods
        else:
            return {"error" : f"event_{request.method}_unsupported"}
    except Exception as e:
        print(e)
        return {"error" : "except_event_module"}
    

   