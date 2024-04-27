from urllib.parse import unquote

def fetch_group(db, group_name):
    try:
        # Attempt to find a group document in the database matching the provided group name and with status set to True
        group  = db.group.find_one({"group_name": unquote(group_name), "status": True})
        
        # If group exists, return its _id and the value of its "share" field, otherwise return False for both values
        if group:
            return group["_id"], group["share"]
        else:
            return False, False
    except:
        return {"error" : "except_fetch_group_module"}
    