from src.CollibraObjects.community import Community

christopher_mulford_com_data = {'id': '5774022f-8fc9-4edc-857a-b96eba505d61',
                                        'name': 'Christopher Mulford',
                                        'parent': None,
                                        'exists_in_env': True,
                                        'createdBy': 'eb527160-2949-414c-9878-c8572bac393d',
                                        'createdOn': 1668595966733,
                                        'lastModifiedBy': 'eb527160-2949-414c-9878-c8572bac393d',
                                        'lastModifiedOn': 1668781611899,
                                        'system': False,
                                        'resourceType': 'Community',
                                        'description': 'Changed with update method'}


def test_existing_community_from_id():
    com = Community(id='5774022f-8fc9-4edc-857a-b96eba505d61')
    assert type(com) == Community
    assert com.get_all_metadata() == christopher_mulford_com_data
    

def test_existing_community_from_name():
    com = Community(name='Christopher Mulford')
    assert type(com) == Community
    assert com.get_all_metadata() == christopher_mulford_com_data


def test_community_not_exist_id():
    com = Community(id='not-an-id')
    assert type(com) == Community
    assert com.get_all_metadata() == {'id': 'not-an-id', 'name': '', 'parent': None, 'exists_in_env': False}


def test_community_not_exist_name():
    com = Community(name='Community doesnt exist')
    assert type(com) == Community
    assert com.get_all_metadata() == {'id': '',
 'name': 'Community doesnt exist',
 'parent': None,
 'exists_in_env': False}