import src.auth
import requests


creds = src.auth.CREDENTIALS


class CollibraObject:
    def get_collibra_metadata_from_name(self):
        '''
        DESCRIPTION: performs a get request on communities endpoint to see if the 
        community exists in the environment.
        '''
        params = {'name': self.name, 'nameMatchMode': 'EXACT'}
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

    def get_collibra_metadata(self, from_attr=None):
        if from_attr == 'id':
            return self.get_collibra_metadata_from_id()
        elif from_attr == 'name':
            return self.get_collibra_metadata_from_name()
        elif self.id != '':
            return self.get_collibra_metadata_from_id()
        else:
            return self.get_collibra_metadata_from_name()


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


    def set_atrrs_from_collibra(self, get_req=None):
        '''
        DESCRIPTION: Creates an attribute for each item returned in the get_request's
        metadata about the community
        '''
        if not get_req:
            get_req = self.get_collibra_metadata()
        for attr in get_req:
            super(type(self), self).__setattr__(attr, get_req[attr])


    def delete_from_collibra(self):
        '''
        DESCRIPTION: Deletes a community from collibra based on input id. Will retain metadata in local object for backup.
        '''
        del_url = self.url + '/removalJobs'
        if self.exists_in_env:
            response = requests.post(del_url, json=[self.id], auth=creds)
            if response.status_code<300:
                print('Success! Here are the details of the community we are going to delete:')
                return response.json()
            else:
                print('Oh no! this did not work. Here is what we heard back:', response.text)
                return None
        else:
            print("Community may not exist in environment. Run Community.check_exists_in_env() and try again.")


    def update_in_collibra(self, dont_update_attrs=[]):
        '''
        DESCRIPTION: Any local changes made can be uploaded to the collibra environment using this function.
        PARAMS:
        - dont_update_attrs: a list of attributes to ignore from update
        '''
        patch_url = self.url + f'/{self.id}'
        attrs = vars(self)
        for attr in dont_update_attrs:
            attrs.pop(attr, None)
        response = requests.patch(patch_url, json=attrs, auth=creds)
        if response.status_code<300:
            print(f'{self.name} successfully updated!')
        else:
            print('Oh no! this did not work. Here is what we heard back:', response.text)

    
    def create_in_collibra(self):
        '''
        DESCRIPTION: Creates community in collibra according to input variables. Checks if the community exists
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
            print(f"Could not create object. {self.name} already exists in collibra. Local object attributes not changed.")


    def get_all_metadata(self):
        '''
        DESCRIPTION: Explodes the vars() built in function to show all objects attributes
        '''
        objs = vars(self).copy()
        for obj in objs:
            if issubclass(type(objs[obj]), CollibraObject):
                objs[obj] = vars(objs[obj])
        return objs


    def get_create_object_params(self):
        params = {'name':self.name,
                 'description':self.description}
        return params