from flask import session
from datetime import datetime, timedelta

def is_api_key_valid():
    if 'api_key' not in session or 'api_key_set_time' not in session:
        return False
    
    set_time = datetime.fromtimestamp(session['api_key_set_time'])
    if datetime.utcnow() - set_time > timedelta(minutes=30):
        return False
    
    return True