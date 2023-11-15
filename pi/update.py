import requests
PARKING_LOT_ID = '20'
SERVER_URL = 'http://10.0.23.52:5000'

def send_increase():
    """Sends a request to the server to increase parking lot capacity."""
    response = requests.post('{}/increase/{}'.format(SERVER_URL, PARKING_LOT_ID), json={'amount': 1})
    return response.ok

def send_decrease():
    """Sends a request to the server to decrease parking lot capacity."""
    response = requests.post('{}/decrease/{}'.format(SERVER_URL, PARKING_LOT_ID), json={'amount': 1})
    return response.ok
