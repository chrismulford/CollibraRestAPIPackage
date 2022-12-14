import src.auth
import requests
if __name__ != "__main__":
    from src.CollibraObjects.collibraObject import CollibraObject
    from src.CollibraObjects.community import Community
else:
    from ...src.CollibraObjects.collibraObject import CollibraObject
    from ...src.CollibraObjects.community import Community


creds = src.auth.CREDENTIALS


class AssetType(CollibraObject):
    url = src.auth.BASE_URL + 'assetTypes'
    def __init__(self,id='', name='', check_exists=True):
        '''
        DESCRIPTION: Initialises the object with a name. If check_exists, then 
        perform a get request to see if this community already exists. If it exists, the 
        set_data_from_existing method will be called to populate the appropriate attributes.
        PARAMS:
        - name*: name of the community (must be unique in env)
        - check_exists: can be used to check if the community alread exists in the environment
        '''
        self.id = id
        self.name = name
        if check_exists:
            self.check_exists_in_env()