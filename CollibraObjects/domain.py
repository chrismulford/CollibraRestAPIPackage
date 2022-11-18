import auth
import requests
if __name__ != "__main__":
    from CollibraObjects.collibraObject import CollibraObject
else:
    from ..CollibraObjects.collibraObject import CollibraObject

creds = auth.CREDENTIALS



class Domain(CollibraObject):
    url = auth.BASE_URL + 'domains'
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


    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        community exists in the environment.
        '''
        params = {'name': self.name, 'nameMatchMode': 'EXACT'}
        return requests.get(url, params=params, auth=creds)


    def check_exists_in_env(self, set_attrs=True):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        community exists in the environment.
        PARAMS:
        - set_attrs: populates the object with metadata from collibra if it exists
        '''
        response = self.get_collibra_metadata_from_name()
        self.exists_in_env = response.json()['total'] > 0
        if self.exists_in_env and set_attrs:
            self.set_atrrs_from_collibra(get_req=response)


    def set_atrrs_from_collibra(self, get_req=None):
        '''
        DESCRIPTION: Creates an attribute for each item returned in the get_request's
        metadata about the community
        '''
        if not get_req:
            get_req = self.get_collibra_metadata_from_name()
        results = get_req.json()['results'][0]
        for attr in results:
            super(type(self), self).__setattr__(attr, results[attr])