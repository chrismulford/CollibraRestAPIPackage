from src.CollibraObjects.community import Community
from src.CollibraObjects.domain import Domain
from src.CollibraObjects.asset import Asset

community = Community(id='5774022f-8fc9-4edc-857a-b96eba505d61')
domain = Domain(id='6f81de67-46fd-4f39-b256-8ed114e89ff4')

def test_asset_from_id():
    asset = Asset(id='6d46b445-9d1b-4ca5-88f6-96d68362eb4a')
    assert asset.id == '6d46b445-9d1b-4ca5-88f6-96d68362eb4a'
    assert asset.name == 'Alpha Dog'
    assert asset.exists_in_env == True
    assert asset.domain.id == '6f81de67-46fd-4f39-b256-8ed114e89ff4'
    assert domain.community.id == '5774022f-8fc9-4edc-857a-b96eba505d61'
    assert asset.type.id == '689da9c4-9019-4f55-bdde-8006d5bfbd72'

def test_asset_from_name():
    asset = Asset(name='Alpha Dog', domain=domain)
    assert asset.id == '6d46b445-9d1b-4ca5-88f6-96d68362eb4a'
    assert asset.name == 'Alpha Dog'
    assert asset.exists_in_env == True
    assert asset.domain.id == '6f81de67-46fd-4f39-b256-8ed114e89ff4'
    assert domain.community.id == '5774022f-8fc9-4edc-857a-b96eba505d61'
    assert asset.type.id == '689da9c4-9019-4f55-bdde-8006d5bfbd72'
