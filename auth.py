import json


with open('creds.json', 'r') as f:
    data = json.load(f)

CREDENTIALS = (data['username'], data['password'])
BASE_URL = data['environment_url']