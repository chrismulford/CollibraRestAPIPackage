import auth
import requests
if __name__ != "__main__":
    from CollibraObjects.collibraObject import CollibraObject
    from CollibraObjects.community import Community
    from CollibraObjects.domain import Domain

else:
    from ..CollibraObjects.collibraObject import CollibraObject
    from ..CollibraObjects.community import Community
    from ..CollibraObjects.domain import Domain

creds = auth.CREDENTIALS


class Asset(CollibraObject):
    url = auth.BASE_URL + 'assets'
    def __init__(self, name, domain, assetType, community, check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the community (must be unique in env)
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.name = name
        if type(domain) == Domain and domain.exists_in_env:
            self.domain = domain
        else:
            self.domain = Domain(domain, community)
            if not self.domain.exists_in_env:
                print(f'"{self.domain.name}" domain does not exist.')
                check_exists = self.domain.exists_in_env
        if check_exists:
            self.check_exists_in_env()


    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on endpoint to see if the 
        object exists in the environment.
        Different from parent as the community is searched.
        '''
        params = {'name': self.name, 'nameMatchMode':'EXACT', 
        'domainId':self.domain.id}
        return requests.get(self.url, params=params, auth=creds)
    
    def set_atrrs_from_collibra(self, get_req=None):
        '''
        DESCRIPTION: Creates an attribute for each item returned in the get_request's
        metadata about the community
        '''
        if not get_req:
            get_req = self.get_collibra_metadata_from_name()
        results = get_req.json()['results'][0]
        results.pop('domain')
        for attr in results:
            super(type(self), self).__setattr__(attr, results[attr])