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
    def __init__(self, id='', asset=None, attributeType=None, value={}, check_exists=True):
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
        self.value = value
        if check_exists:
            self.check_exists_in_env()
        if self.exists_in_env:
            self.asset = Asset(id=self.asset['id'])
            self.type = AttributeType(id=self.type['id'])

    def check_exists_in_env(self, set_attrs=True):
        '''
        DESCRIPTION: performs a get request on endpoint to see if the 
        object exists in the environment.
        PARAMS:
        - set_attrs: populates the object with metadata from collibra if it exists
        '''
        response = self.get_collibra_metadata_from_id()
        if self.exists_in_env and set_attrs:
            self.set_atrrs_from_collibra(get_req=response)