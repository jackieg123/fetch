from requests import Response
import json
from enum import Enum


class Dog:
    # options = None
    # contact = None  # contact includes address, email, phone
    # description = None
    photos = None
    name = None
    gender = None
    status = None

    def set_name(self, name):
        self.name = name

    def set_photos(self, photos):
        self.photos = photos

    def set_gender(self, gender):
        self.gender = gender

    def set_status(self, status):
        self.status = status


class DogBuilder:
    def __init__(self, response: dict):
        self.response = response

    def run(self):
        dog = Dog()
        dog.set_name(self.response['name'])
        dog.set_photos(self.response['photos'])
        dog.set_gender(self.response['gender'])
        dog.set_status(self.response['status'])
        return dog


class ResponseType(Enum):
    ACCESS_TOKEN = 'access_token'
    ANIMALS = 'animals'


class PetfinderResponse:
    def __init__(self, response: Response, response_type: ResponseType):
        self.response = response
        assert isinstance(response_type, ResponseType)
        self.response_type = response_type.value

    def load(self):
        decoded_json = self.response.content.decode('ascii')
        return json.loads(decoded_json)[self.response_type]
