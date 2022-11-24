import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
    from src.CollibraObjects.community import Community
    from src.CollibraObjects.domainType import DomainType
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject
    from ...src.CollibraObjects.community import Community
    from ...src.CollibraObjects.domainType import DomainType

creds = src.auth.CREDENTIALS


class Domain(CollibraObject):
    url = src.auth.BASE_URL + 'domains'
    def __init__(self, id='', name='', community:Community=None, domainType:DomainType=None, check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - id*: unique id of the Domain. Required if name not specified.
        - name*: name of the Domain (must be unique in env). Required if id not specified.
        - community*: Community object for the parent community of the domain. Required if id not specified.
        - domainType: DomainType object of the Domain to help ensure it is unique.
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        if check_exists:
            if self.id != '':
                self.check_exists_in_env()
                self.community = Community(id=self.community['id'])
                self.type = DomainType(id=self.type['id'])
            else:
                self.name = name
                if type(community) == Community: 
                    self.community = community
                    if not community.exists_in_env:
                        raise ValueError(f'Community does not exist: \n {self.community.get_all_attributes()}')
                self.check_exists_in_env()
                if type(domainType) == DomainType:
                    self.type = domainType
                    if not domainType.exists_in_env:
                        raise ValueError(f'DomainType does not exist: \n {self.type.get_all_attributes()}')
                else:
                    self.type = DomainType(id=self.type['id'])
                
        else:
            self.name = name
                

            
    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        community exists in the environment.
        '''
        params = {'name': self.name, 'nameMatchMode': 'EXACT', 'communityId':self.community.id}
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
        if 'community' in vars(self):
            get_req.pop('community')
        if 'type' in vars(self):
            get_req.pop('type')
        for attr in get_req:
            super(type(self), self).__setattr__(attr, get_req[attr])