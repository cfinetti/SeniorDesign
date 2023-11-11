import requests

SERVER_URL = 'http://<server_ip>:<port>'

def send_increase():
    """Sends a request to the server to increase parking lot capacity."""
    response = requests.post(f'{SERVER_URL}/increase', json={'amount': 1})
    return response.ok

def send_decrease():
    """Sends a request to the server to decrease parking lot capacity."""
    response = requests.post(f'{SERVER_URL}/decrease', json={'amount': 1})
    return response.ok
