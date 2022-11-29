import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
    from src.CollibraObjects.asset import Asset
    from src.CollibraObjects.attributeType import AttributeType
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject
    from ...src.CollibraObjects.asset import Asset
    from ...src.CollibraObjects.attributeType import AttributeType

creds = src.auth.CREDENTIALS


class Attribute(CollibraObject):
    url = src.auth.BASE_URL + 'attributes'
    def __init__(self, id='', asset=None, attributeType=None, description='', check_exists=True):
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
        self.asset = asset
        self.type = attributeType
        self.description = description
        if check_exists:
            self.check_exists_in_env()
        #if self.exists_in_env:
        #    self.asset = Asset(id=self.asset['id'])
        #    self.type = AttributeType(id=self.type['id'])

    def check_exists_in_env(self, set_attrs=True):
        '''
        DESCRIPTION: performs a get request on endpoint to see if the 
        object exists in the environment.
        PARAMS:
        - set_attrs: populates the object with metadata from collibra if it exists
        '''
        response = self.get_collibra_metadata()
        if self.exists_in_env and set_attrs:
            self.set_atrrs_from_collibra(get_req=response)


    def delete_from_collibra(self):
        '''
        DESCRIPTION: Deletes an attribute from collibra based on input id. Will retain metadata in local object for backup.
        '''
        del_url = self.url + f'/{self.id}'
        if self.exists_in_env:
            response = requests.delete(del_url, auth=creds)
            if response.status_code<300:
                print('Success! Here are the details of the attribute we are going to delete:')
                return response.json()
            else:
                print('Oh no! this did not work. Here is what we heard back:', response.text)
                return None
        else:
            print("Attribute may not exist in environment. Run Attribute.check_exists_in_env() and try again.")

    
    def get_create_object_params(self):
        params = {'assetId':self.asset.id,
                'typeId':self.type.id,
                'value': self.description}
        return params

    def create_in_collibra(self):
        f'''
        DESCRIPTION: Creates {type(self)} in collibra according to input variables. Checks if the {type(self)} exists
        first, will set attributes if success but will not change attributes of local object if fails.
        '''
        self.check_exists_in_env(set_attrs=False)
        if not self.exists_in_env:
            params = self.get_create_object_params()
            response = requests.post(self.url, json=params,auth=creds)
            if response.ok:
                self.set_atrrs_from_collibra()
                print('Success!')
            else:
                print('Oh no! this did not work. Here is what we heard back:', response.text)
            
        else:
            print(f"Could not create object. {self.value} already exists in collibra. Local object attributes not changed.")

    def get_collibra_metadata_from_id(self):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        community exists in the environment.
        '''
        resp = requests.get(f'{self.url}/{self.id}', auth=creds)
        if resp.status_code > 300:
            self.exists_in_env = False
            return None
        else:
            self.exists_in_env = True
            return resp.json()


    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        object exists in the environment.
        '''
        params = {'assetId': self.asset.id, 'typeID': self.type.id}
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