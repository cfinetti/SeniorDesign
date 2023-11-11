import requests

SERVER_URL = 'http://172.31.56.243:5000'

def send_increase():
    """Sends a request to the server to increase parking lot capacity."""
    response = requests.post('{}/increase'.format(SERVER_URL), json={'amount': 1})
    return response.ok

def send_decrease():
    """Sends a request to the server to decrease parking lot capacity."""
    response = requests.post('{}/decrease'.format(SERVER_URL), json={'amount': 1})
    return response.ok
