from urllib.parse import unquote

def fetch_calendar(db, calendar_name, user_id):
    try:
        # Attempt to find a calendar document in the database matching the provided calendar name and with status set to True
        calendar = db.calendar.find_one({"calendar_name": unquote(calendar_name), "status": True})
        
        # Check if calendar exists and user_id matches the owner's user_id
        owner = str(user_id) == str(calendar["user_id"]) if calendar else False

        # If calendar exists, return its _id and owner status, otherwise return False for both
        if calendar:
            return calendar["_id"], owner
        else:
            return False, False
    except:
        return {"error" : "except_fetch_users_module"}
    