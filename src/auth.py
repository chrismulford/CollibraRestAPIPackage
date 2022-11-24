import json


with open('creds.json', 'r') as f:
    data = json.load(f)

CREDENTIALS = (data['username'], data['password'])
if data['environment_url'][-1] == '/':
    data['environment_url'] = data['environment_url'][:-1]
BASE_URL = data['environment_url'] + '/rest/2.0/'