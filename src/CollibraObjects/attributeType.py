import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject

creds = src.auth.CREDENTIALS


class AttributeType(CollibraObject):
    url = src.auth.BASE_URL + 'attributeTypes'
    def __init__(self, id='', name='', kind='',check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the attribute type (must be unique in environment). Required if id not specified.
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        self.name = name
        self.kind = kind
        if check_exists:
            self.check_exists_in_env()
        self.resource_type_to_kind()

    def resource_type_to_kind(self):
        if self.exists_in_env:
            self.kind = self.resourceType[:-13].upper()
            if self.kind == 'SINGLEVALUELIST':
                self.kind = 'SINGLE_VALUE_LIST'
            if self.kind == 'MULTIVALUELIST':
                self.kind = 'MULTI_VALUE_LIST'

    def delete_from_collibra(self):
        '''
        DESCRIPTION: Deletes an attribute type from collibra based on input id. 
        Will retain metadata in local object for backup.
        '''
        del_url = self.url + f'/{self.id}'
        if self.exists_in_env:
            response = requests.delete(del_url, auth=creds)
            if response.status_code<300:
                print('Success! Here are the details of the attribute type we are going to delete:')
                return response.json()
            else:
                print('Oh no! this did not work. Here is what we heard back:', response.text)
                return None
        else:
            print("Attribute may not exist in environment. Run Attribute.check_exists_in_env() and try again.")

    
    def get_create_object_params(self):
        params = {'name':self.name,
                'kind':self.kind}
        return params