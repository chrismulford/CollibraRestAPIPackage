import auth
import requests
if __name__ != "__main__":
    from CollibraObjects.collibraObject import CollibraObject
else:
    from ..CollibraObjects.collibraObject import CollibraObject


creds = auth.CREDENTIALS


class Community(CollibraObject):
    url = auth.BASE_URL + 'communities'
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


    def available_params(self):
            '''
            DESCRIPTION: shows the available attributes for the given object
            '''
            return ['parentId' ,'createdBy' ,'createdOn' ,'lastModifiedBy' ,'lastModifiedOn' ,
            'system' ,'resourceType' ,'description']


    
    

    
