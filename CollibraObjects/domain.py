import auth
import requests
if __name__ != "__main__":
    from CollibraObjects.collibraObject import CollibraObject
    from CollibraObjects.community import Community
    from CollibraObjects.domainType import DomainType
else:
    from ..CollibraObjects.collibraObject import CollibraObject
    from ..CollibraObjects.community import Community
    from ..CollibraObjects.domainType import DomainType

creds = auth.CREDENTIALS


class Domain(CollibraObject):
    url = auth.BASE_URL + 'domains'
    def __init__(self, id='', name='', domainType='', community='', check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the community (must be unique in env)
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        if self.id != '':
            self.check_exists_in_env()
            self.community = Community(id=self.community['id'])
            self.type = DomainType(id=self.type['id'])
        else:
            self.name = name
            if type(community) == Community and community.exists_in_env:
                self.community = community
            else:
                self.community = Community(name=community)
                if not self.community.exists_in_env:
                    print(f'"{self.community.name}" community does not exist.')
                    check_exists = self.community.exists_in_env
            if type(domainType) == DomainType and domainType.exists_in_env:
                self.type = domainType
            elif domainType != '':
                self.type = DomainType(name=domainType)
                if not self.type.exists_in_env:
                    print(f'"{self.type.name}" DomainType does not exist.')
                    check_exists = self.type.exists_in_env
            else:
                self.check_exists_in_env()
                self.type = DomainType(id=self.type['id'])
                check_exists=False
            if check_exists:
                self.check_exists_in_env()
                

            
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
            self.exists_in_env = True
            return resp.json()['results'][0]


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