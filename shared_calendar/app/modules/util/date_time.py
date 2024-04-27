from datetime import datetime

# Function to convert date string to datetime object
def date_time_(dt):
    return datetime.strptime(dt, '%Y-%m-%d %H:%M')