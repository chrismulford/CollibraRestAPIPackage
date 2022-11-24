import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
    from src.CollibraObjects.community import Community
    from src.CollibraObjects.domain import Domain
    from src.CollibraObjects.assetType import AssetType
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject
    from ...src.CollibraObjects.community import Community
    from ...src.CollibraObjects.domain import Domain
    from ...src.CollibraObjects.assetType import AssetType

creds = src.auth.CREDENTIALS


class Asset(CollibraObject):
    url = src.auth.BASE_URL + 'assets'
    def __init__(self,id='', name='', domain:Domain=None, assetType=None, check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - id*: unique id of the Asset. required if name not specified.
        - name*: name of the Asset (must be unique in domain). Required if id not specified.
        - domain*: Domain object in which the asset exists
        - assetType: The AssetType object of the asset to help ensure it is unique
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        if self.id != '':
            self.check_exists_in_env()
            self.domain = Domain(id=self.domain['id'])
            self.type = AssetType(id=self.type['id'])
        else:
            self.name = name
            '''
            if type(community) == Community: 
                self.community = community
                if not community.exists_in_env:
                    raise ValueError(f'Community does not exist: \n {self.community.get_all_attributes()}')
            '''
            if type(domain) == Domain:
                self.domain = domain
                if not domain.exists_in_env:
                    raise ValueError(f'Domain does not exist: \n {self.domain.get_all_metadata()}')
            if type(assetType) == AssetType:
                self.type = assetType
                if not assetType.exists_in_env:
                    raise ValueError(f'AssetType does not exist: \n {self.type.get_all_attributes()}')
            self.check_exists_in_env()


    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on endpoint to see if the 
        object exists in the environment.
        Different from parent as the community is searched.
        '''
        params = {'name': self.name, 'nameMatchMode':'EXACT', 
        'domainId':self.domain.id}
        resp = requests.get(self.url, params=params, auth=creds)
        if resp.status_code > 300 or resp.json()['total'] < 0:
            self.exists_in_env = False
            return None
        else:
            if resp.json()['total'] > 0:
                self.exists_in_env = True
                return resp.json()['results'][0]
            else:
                self.exists_in_env = False
    
    def set_atrrs_from_collibra(self, get_req=None):
        '''
        DESCRIPTION: Creates an attribute for each item returned in the get_request's
        metadata about the community
        '''
        if not get_req:
            get_req = self.get_collibra_metadata()
        if 'domain' in vars(self):
            get_req.pop('domain')
        if 'type' in vars(self):
            get_req.pop('type')
        for attr in get_req:
            super(type(self), self).__setattr__(attr, get_req[attr])