import json
from base64 import b64encode

import requests

# response = requests.get(url='http://127.0.0.1:5001/register_user',
#                         headers={'Authorization': 'Basic ' + b64encode(
#                             f"user:0".encode()).decode()})
# print(json.loads(response.text))
data = {'email': 'a',
        'password': 'b',
        'first_name': 'c',
        'last_name': 'd',
        'phone_number': 'e',
        'renter_address': 'f',
        'business_sphere': 'g'}
response = requests.post(url='http://127.0.0.1:5001/register_renter', json=data)
print(response)
