import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject


creds = src.auth.CREDENTIALS


class Community(CollibraObject):
    url = src.auth.BASE_URL + 'communities'
    def __init__(self, id='', name='', parentCommunity=None, description='',check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the community (must be unique in env)
        - parentCommunity: Community object of the parent of the current community
        - description: Displayed description of the community. Will be overwritten if community exists already
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        self.name = name
        self.parent = parentCommunity
        self.description = description
        if check_exists:
            self.check_exists_in_env()


    def available_params(self):
            '''
            DESCRIPTION: shows the available attributes for the given object
            '''
            return ['parentId' ,'createdBy' ,'createdOn' ,'lastModifiedBy' ,'lastModifiedOn' ,
            'system' ,'resourceType' ,'description']
    
    def get_create_object_params(self):
        if self.parent:
                parentId = self.parent.id
        else:
            parentId = ''
        params = {'parentId':parentId,
                'name':self.name,
                'description':self.description}
        return params

    
