import os
from unittest import TestCase
from requests import HTTPError
from fetch_api.entities import Dog
from fetch_api.repository import PetfinderRepository, get_access_token


class TestPetfinderRepository(TestCase):
    def test_get_access_token_returns_token_as_string(self):
        client_id = os.environ['PETFINDER_KEY']
        client_secret = os.environ['PETFINDER_SECRET']
        token = get_access_token(client_id, client_secret)
        self.assertIsInstance(token, str)

    def test_get_dogs_by_location_returns_list_of_adoptable_dogs(self):
        location = '23220'
        petfinder_repository = PetfinderRepository(location)
        dogs = petfinder_repository.get_dogs_by_location()
        self.assertIsInstance(dogs, list)

        for dog in dogs:
            self.assertIsInstance(dog, Dog)
            self.assertIsNotNone(dog.name)
            self.assertIsNotNone(dog.photos)
            self.assertIsNotNone(dog.gender)
            self.assertEqual('adoptable', dog.status)

    def test_get_dogs_by_location_raises_http_error_for_bad_request(self):
        location = 'not a valid location!'
        petfinder_repository = PetfinderRepository(location)
        with self.assertRaises(HTTPError):
            petfinder_repository.get_dogs_by_location()
