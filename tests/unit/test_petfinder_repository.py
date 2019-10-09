from unittest import TestCase, mock

import responses

from fetch_api.repository import PetfinderRepository
from fetch_api.entities import Dog


class TestPetfinderRepository(TestCase):
    def setUp(self):
        self.petfinder_repo = PetfinderRepository('location')
        self.get_access_token = mock.patch('fetch_api.repository.get_access_token')
        self.patch_of_get_access_token = self.get_access_token.start()
        self.patch_of_get_access_token.return_value = 'token'

    def tearDown(self):
        self.get_access_token.stop()

    def test_init_throws_error_if_petfinder_key_not_found(self):
        with self.assertRaises(KeyError), mock.patch.dict('os.environ', {'PETFINDER_SECRET': 'secret'}, clear=True):
            PetfinderRepository('location')

    def test_init_throws_error_if_petfinder_secret_not_found(self):
        with self.assertRaises(KeyError), mock.patch.dict('os.environ', {'PETFINDER_KEY': 'key'}, clear=True):
            PetfinderRepository('location')

    def test_init_calls_get_access_token_once(self):
        PetfinderRepository('location')
        self.patch_of_get_access_token.assert_called_once()

    def test_init_sets_headers(self):
        petfinder_repository = PetfinderRepository('location')
        expected_headers = {"Authorization": f"Bearer token"}
        self.assertEqual(expected_headers, petfinder_repository.headers)

    def test_init_sets_url_root(self):
        petfinder_repository = PetfinderRepository('location')
        self.assertEqual('https://api.petfinder.com/v2', petfinder_repository.url_root)

    def test_init_sets_location(self):
        location = 'some_location'
        petfinder_repository = PetfinderRepository(location)
        self.assertEqual(location, petfinder_repository.location)

    @responses.activate
    def test_get_dogs_by_location_throws_error_if_response_code_not_200(self):
        with self.assertRaises(Exception):
            petfinder_repository = PetfinderRepository('some')
            get_dogs_url = "https://api.petfinder.com/v2/animals?type=dog&status=adoptable&distance=50&location=some"
            responses.add(responses.GET, get_dogs_url, json={}, status=400)
            petfinder_repository.get_dogs_by_location()

    @responses.activate
    def test_compile_data_into_list_of_dogs_returns_list_of_dogs(self):
        animals = {'animals': [
            {'id': 45243763, 'organization_id': 'VA803',
             'url': 'https://www.petfinder.com/dog/chester-45243763/va/chesterfield/blue-ridge-bull-'
                    'terrier-rescue-va803/?referrer_id=b20db8b0-afd6-420d-ab9f-482de071a029',
             'type': 'Dog', 'species': 'Dog',
             'breeds': {'primary': 'Bull Terrier', 'secondary': None, 'mixed': False, 'unknown': False},
             'colors': {'primary': 'White / Cream', 'secondary': None, 'tertiary': None}, 'age': 'Adult',
             'gender': 'Male', 'size': 'Medium', 'coat': 'Short',
             'attributes': {'spayed_neutered': False, 'house_trained': False, 'declawed': None,
                            'special_needs': False,
                            'shots_current': True},
             'environment': {'children': True, 'dogs': True, 'cats': None},
             'tags': ['Happy', 'Loving', 'Energetic'], 'name': 'Chester',
             'description': 'Chester is looking for a foster or furever home through Blue Ridge Bull '
                            'Terrier Rescue! Chester is patiently waiting in...',
             'photos': [
                 {
                     'small': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/1/?bust=1562986750&width=100',
                     'medium': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/1/?bust=1562986750&width=300',
                     'large': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/1/?bust=1562986750&width=600',
                     'full': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/1/?bust=1562986750'},
                 {
                     'small': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/2/?bust=1562986756&width=100',
                     'medium': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/2/?bust=1562986756&width=300',
                     'large': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/2/?bust=1562986756&width=600',
                     'full': 'https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/45243763/2/?bust=1562986756'}],
             'status': 'adoptable', 'published_at': '2019-07-13T03:02:23+0000',
             'contact': {'email': 'info.brbtc@gmail.com', 'phone': '(703) 831-7323',
                         'address': {'address1': None, 'address2': None, 'city': 'Chesterfield',
                                     'state': 'VA',
                                     'postcode': '23832', 'country': 'US'}},
             '_links': {'self': {'href': '/v2/animals/45243763'}, 'type': {'href': '/v2/types/dog'},
                        'organization': {'href': '/v2/organizations/va803'}}},
            {'id': 45242846, 'organization_id': 'VA182',
             'url': 'https://www.petfinder.com/dog/honey2-45242846/va/louisa/'
                    'louisa-humane-society-va182/?referrer_id=b20db8b0-afd6-420d-ab9f-482de071a029',
             'type': 'Dog', 'species': 'Dog',
             'breeds': {'primary': 'Pomeranian', 'secondary': None, 'mixed': False, 'unknown': False},
             'colors': {'primary': None, 'secondary': None, 'tertiary': None}, 'age': 'Senior',
             'gender': 'Female', 'size': 'Small', 'coat': None,
             'attributes': {'spayed_neutered': True, 'house_trained': True, 'declawed': None,
                            'special_needs': False, 'shots_current': True},
             'environment': {'children': None, 'dogs': True, 'cats': True}, 'tags': [], 'name': 'Honey2',
             'description': 'Honey and Boomer are a bonded pair and must be adopted together.'
                            '&amp;#10;&amp;#10;The Adoption Process&amp;#10;&amp;#10;&amp;#10; '
                            'If you are ready to meet...',
             'photos': [], 'status': 'adoptable', 'published_at': '2019-07-13T02:38:14+0000',
             'contact': {'email': 'info@louisahumanesociety.com', 'phone': None,
                         'address': {'address1': 'P.O. Box 1837', 'address2': None, 'city': 'Louisa',
                                     'state': 'VA', 'postcode': '23093', 'country': 'US'}},
             '_links': {'self': {'href': '/v2/animals/45242846'}, 'type': {'href': '/v2/types/dog'},
                        'organization': {'href': '/v2/organizations/va182'}}}

        ]
        }
        petfinder_repository = PetfinderRepository('someLocation')

        get_dogs_url = "https://api.petfinder.com/v2/animals?type=dog&status=adoptable&distance=50&location=someLocation"
        responses.add(responses.GET, get_dogs_url,
                      json=animals, status=200)

        dogs = petfinder_repository.get_dogs_by_location()
        self.assertIsInstance(dogs, list)

        for dog in dogs:
            self.assertIsInstance(dog, Dog)
            self.assertIsNotNone(dog.name)
            self.assertIsNotNone(dog.photos)
            self.assertIsNotNone(dog.gender)
            self.assertEqual('adoptable', dog.status)
