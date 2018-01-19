import requests
from requests.auth import HTTPBasicAuth
import json


class StoreSamples(object):

    top_level_url = "http://localhost:8080/Plone"
    username = "admin"
    password = "leAzvzwbUAXT"  # secret
    project_uid = None
    sample_types = None
    response = None

    def __init__(self, project_id="project-1"):
        auth = HTTPBasicAuth(self.username, self.password)
        self.auth = auth

        project_url = self.top_level_url + "/@@API/v2/Project?id=%s" % project_id
        project_response = requests.get(project_url, auth=self.auth)

        if project_response.status_code == 200:
            self.project_data = project_response.json()
        else:
            raise('failed to retrieve project %s' % project_id)

        sample_types_url = self.top_level_url + "/@@API/v2/SampleType"
        sample_types_response = requests.get(sample_types_url, auth=self.auth)

        if sample_types_response.status_code == 200:
            self.sample_types_data = sample_types_response.json()
        else:
            raise 'failed to retrieve sample types'

    def set_project_uid(self, project_id="project-1"):

        for item in self.project_data['items']:
            if item['id'] == project_id:
                self.project_uid = item['uid']
                break

    def set_sample_types(self):

        sample_types = {}
        for item in self.sample_types_data['items']:
            sample_types[item['title']] = item['uid']

        self.sample_types = sample_types

    def create_sample(self, data):

        body = {"BODY": json.dumps(data)}

        url = self.top_level_url  + '/@@API/v2/create/' + self.project_uid
        response = requests.post(url, data=body, auth=self.auth)

        return response




if __name__ == "__main__":
    store_samples = StoreSamples()
    store_samples.set_project_uid()
    store_samples.set_sample_types()

    create_samples_data = {
        "portal_type": "Sample",
        "SampleID": "id102157",
        "title": "def0037",
        "Project": store_samples.project_uid,
        "SampleType": "Urine",
        "Barcode": "bar00427",
        "StorageLocation": "Room-3.Freezer-1.Box-02.26",
        "Volume": "20.00",
        "Unit": "ml",
        "APISource": "odk",
    }

    sample_response = store_samples.create_sample(create_samples_data)

    print('------------')
    print(store_samples.project_uid)
    print(store_samples.sample_types)
    print('------------')

    print(sample_response.json())
    print('------------')



