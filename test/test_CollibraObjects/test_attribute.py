from src.CollibraObjects.community import Community
from src.CollibraObjects.domain import Domain
from src.CollibraObjects.asset import Asset
from src.CollibraObjects.attribute import Attribute
from src.CollibraObjects.attributeType import AttributeType


attr = Attribute(asset=Asset(name='Doom Bar', 
domain=Domain(name='Chris Beer Collection',community=Community(name='Christopher Mulford'))),
attributeType=AttributeType(id='86c77975-34c1-4736-9c77-75efbf841675'),
description='Amber Ale')

def test_get_attr_from_name():
    print(attr)
    assert attr.id == 'e44f898f-1806-48ae-b034-ce71d8fcc454'
    assert attr.exists_in_env == True
    assert attr.asset.id == 'd154493e-f5be-442d-8413-df1c891cdeb9'
    assert attr.type.id == '86c77975-34c1-4736-9c77-75efbf841675'


attr = Attribute(id='e44f898f-1806-48ae-b034-ce71d8fcc454')
def test_get_attr_from_id():
    print(attr)
    assert attr.id == 'e44f898f-1806-48ae-b034-ce71d8fcc454'
    assert attr.exists_in_env == True
    assert attr.asset.id == 'd154493e-f5be-442d-8413-df1c891cdeb9'
    assert attr.type.id == '86c77975-34c1-4736-9c77-75efbf841675'