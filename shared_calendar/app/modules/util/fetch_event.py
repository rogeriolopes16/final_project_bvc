from urllib.parse import unquote
from modules.event import date_time_

def fetch_event(db, event_name, date):
    try:
        # Attempt to find an event document in the database matching the provided event name and with status set to True
        event  = db.event.find_one({"event_name": unquote(event_name), "start_date_time": date_time_(date), "status": True})
        
        # If event exists, return its _id, otherwise return False
        if event:
            return event["_id"]
        else:
            return False
    except:
        return {"error" : "except_fetch_event_module"}
    