def fetch_user(db, email):
    try:
        # Attempt to find a user document in the database matching the provided email and with status set to True
        user = db.users.find_one({"email": email, "status": True})
        
        # If user exists, return its _id and the value of its "admin" field, otherwise return False for both values
        if user:
            return user["_id"], user["admin"]
        else:
            return False, False
    except:
        return {"error" : "except_fetch_user_module"}
    