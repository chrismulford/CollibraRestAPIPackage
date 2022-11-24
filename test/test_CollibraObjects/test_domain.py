from src.CollibraObjects.community import Community
from src.CollibraObjects.domain import Domain
from src.CollibraObjects.domainType import DomainType
from pytest import raises


dom = Domain(id='6f81de67-46fd-4f39-b256-8ed114e89ff4')
def test_existing_domain_from_id():
    assert type(dom) == Domain
    assert dom.name == 'Punk Beer Collection'
    assert dom.id == '6f81de67-46fd-4f39-b256-8ed114e89ff4'
    assert dom.exists_in_env == True
    assert dom.community.id == '5774022f-8fc9-4edc-857a-b96eba505d61'
    assert dom.community.name == 'Christopher Mulford'
    assert dom.type.name == 'Business Asset Domain'
    assert dom.type.id == '00000000-0000-0000-0000-000000030002'


dom = Domain(name='Punk Beer Collection', community=Community(name='Christopher Mulford'))
def test_existing_domain_from_name():
    assert type(dom) == Domain
    assert dom.name == 'Punk Beer Collection'
    assert dom.id == '6f81de67-46fd-4f39-b256-8ed114e89ff4'
    assert dom.exists_in_env == True
    assert dom.community.id == '5774022f-8fc9-4edc-857a-b96eba505d61'
    assert dom.community.name == 'Christopher Mulford'
    assert dom.type.name == 'Business Asset Domain'
    assert dom.type.id == '00000000-0000-0000-0000-000000030002'

def test_object_types_within_domain():
    assert type(dom) == Domain
    assert type(dom.community) == Community
    assert type(dom.type) == DomainType


def test_community_not_exist():
    with raises(ValueError):
        dom = Domain(name='Punk Beer Collection', community=Community(name='Not a real community'))


def test_domainType_not_exist():
    with raises(ValueError):
        dom = Domain(name='Punk Beer Collection', community=Community(name='Not a real community'),
        domainType=DomainType(name='Not Real'))

