import json

# TODO: turn into a class and allow url to change

with open('creds.json', 'r') as f:
    data = json.load(f)

CREDENTIALS = (data['username'], data['password'])
BASE_URL = data['environment_url']