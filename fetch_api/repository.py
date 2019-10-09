import os

import requests

from fetch_api.entities import DogBuilder, PetfinderResponse, ResponseType
from typing import List, Dict

def get_access_token(client_id, client_secret):
    token_request = {'grant_type': 'client_credentials',
                     'client_id': client_id,
                     'client_secret': client_secret}
    token_response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=token_request)
    token = PetfinderResponse(token_response, ResponseType.ACCESS_TOKEN).load()
    return token


class PetfinderRepository:
    def __init__(self, location: str):
        # todo This block gets headers. Does it belong elsewhere?
        client_id = os.environ['PETFINDER_KEY']
        client_secret = os.environ['PETFINDER_SECRET']
        token = get_access_token(client_id, client_secret)
        self.headers = {"Authorization": f"Bearer {token}"}

        self.url_root = "https://api.petfinder.com/v2"
        self.location = location  # todo Validate location. It must be a zip or state

    @staticmethod
    def compile_data_into_list_of_dogs(data_for_dogs: List[Dict]):
        dogs = []
        for item in data_for_dogs:
            builder = DogBuilder(item)
            dog = builder.run()
            dogs.append(dog)
        return dogs

    def get_dogs_by_location(self):
        url = f'{self.url_root}/animals?type=dog&status=adoptable&distance=50&location={self.location}'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = PetfinderResponse(response, ResponseType.ANIMALS).load()

        dogs = self.compile_data_into_list_of_dogs(data)
        return dogs
