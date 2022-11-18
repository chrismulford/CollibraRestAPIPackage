import json

# TODO: turn into a class and allow url to change

BASE_URL = 'https://kubrick-dev.collibra.com/rest/2.0/'

with open('creds.json', 'r') as f:
    data = json.load(f)

CREDENTIALS = (data['username'], data['password'])