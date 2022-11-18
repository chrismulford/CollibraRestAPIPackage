import auth
import requests


creds = auth.CREDENTIALS
url = auth.BASE_URL + 'communities'

class Community:
    def __init__(self, name, check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the community (must be unique in env)
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.name = name
        if check_exists:
            self.check_exists_in_env()

    def check_exists_in_env(self):
        params = {'name': self.name, 'nameMatchMode': 'EXACT'}
        response = requests.get(url, params=params, auth=creds)
        self.exists_in_env = response.status_code == 200
        if self.exists_in_env:
            self.set_data_from_existing(get_req=response)

    def set_data_from_existing(self, get_req=None):
        results = get_req.json()['results'][0]
        for attr in results:
            super(Community, self).__setattr__(attr, results[attr])

    def available_params(self):
        return ['parent' ,'createdBy' ,'createdOn' ,'lastModifiedBy' ,'lastModifiedOn' ,
        'system' ,'resourceType' ,'description']


if __name__ == '__main__':
    com = Community('Christopher Mulford')
    print(vars(com))
