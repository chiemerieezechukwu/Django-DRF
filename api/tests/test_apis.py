import random
from copy import deepcopy
from unittest.mock import patch
from django.shortcuts import reverse
from django.test import TransactionTestCase
from api.models import Car


EXT_API_RETURN_VALUE = {
    'Count': 4,
    'Message': 'Response returned successfully',
    'SearchCriteria': 'Make:Volkswagen',
    'Results': [
        {'Make_ID': 482, 'Make_Name': 'VOLKSWAGEN', 'Model_ID': 3133, 'Model_Name': 'Golf'},
        {'Make_ID': 482, 'Make_Name': 'VOLKSWAGEN', 'Model_ID': 3134, 'Model_Name': 'Passat'},
        {'Make_ID': 482, 'Make_Name': 'VOLKSWAGEN', 'Model_ID': 3135, 'Model_Name': 'Phaeton'},
        {'Make_ID': 482, 'Make_Name': 'VOLKSWAGEN', 'Model_ID': 1951, 'Model_Name': 'Routan'},
    ]
}


class TestCarsAPI(TransactionTestCase):

    reset_sequences = True
    
    @patch('api.services.get_models_for_make')
    def setUp(self, ext_api):
        ext_api.return_value = deepcopy(EXT_API_RETURN_VALUE)

        self.client.post(reverse('cars_view'), {
            'make': 'VOLKSWAGEN',
            'model': 'Golf'
        })

    def tearDown(self):
        Car.objects.all().delete()

    @patch('api.services.get_models_for_make')
    def test_car_entry_creation(self, ext_api):
        ext_api.return_value = deepcopy(EXT_API_RETURN_VALUE)

        response = self.client.post(reverse('cars_view'), {
            'make': 'VOLKSWAGEN',
            'model': 'Passat'
        })

        self.assertDictEqual(response.json(), {
            'id': 2,
            'make': 'VOLKSWAGEN',
            'model': 'Passat',
            'avg_rating': '0.0'
        })

        self.assertEqual(Car.objects.count(), 2)

        # Malformed request should return 400
        err_response = self.client.post(reverse('cars_view'), {
            'make': 'NonExistent',
            'model': 'NonExistent'
        })

        self.assertEqual(err_response.status_code, 400)

    def test_get_cars_list(self):
        response = self.client.get(reverse('cars_view'))
        
        self.assertListEqual(response.json(), [
            {'avg_rating': '0.0', 'id': 1, 'make': 'VOLKSWAGEN', 'model': 'Golf'}
        ])

        self.assertEqual(len(response.data), 1)

class TestCarDeleteAPI(TransactionTestCase):

    reset_sequences = True

    @patch('api.services.get_models_for_make')
    def setUp(self, ext_api):
        ext_api.return_value = deepcopy(EXT_API_RETURN_VALUE)

        self.client.post(reverse('cars_view'), {
            'make': 'VOLKSWAGEN',
            'model': 'Golf'
        })

    def tearDown(self):
        Car.objects.all().delete()

    def test_delete_car_instance(self):
        # Trying to delete an instance that does not exist should return 404
        err_response = self.client.delete(reverse('cars_details_view', kwargs={'car_id': 2}))
        self.assertEqual(err_response.status_code, 404)

        self.assertEqual(Car.objects.count(), 1)

        # deleting one that exists
        response = self.client.delete(reverse('cars_details_view', kwargs={'car_id': 1}))
        self.assertEqual(response.status_code, 204)

        self.assertEqual(Car.objects.count(), 0)


class TestRatePopularAPIs(TransactionTestCase):

    reset_sequences = True

    @patch('api.services.get_models_for_make')
    def setUp(self, ext_api):
        ext_api.return_value = deepcopy(EXT_API_RETURN_VALUE)
        car_list = [
            {'make': 'VOLKSWAGEN', 'model': 'Golf'},
            {'make': 'VOLKSWAGEN', 'model': 'Routan'},
            {'make': 'VOLKSWAGEN', 'model': 'Phaeton'},
        ]
        for car in car_list:
            # add car to db
            self.client.post(reverse('cars_view'), car)

    def tearDown(self):
        Car.objects.all().delete()

    def test_add_ratings_popular_cars(self):
        self.assertEqual(Car.objects.count(), 3)

        response = self.client.get(reverse('cars_view'))
        cars = response.json()

        for car in cars:
            rating_list = [random.randint(1, 5) for _ in range(random.randint(5, 20))]

            for rate in rating_list:
                self.client.post(reverse('ratings_view'), {'car_id': car['id'], 'rating': rate})

            car_detail = self.client.get(reverse('cars_details_view', kwargs={'car_id': car['id']})).json()
            self.assertAlmostEqual(sum(rating_list)/len(rating_list), float(car_detail['avg_rating']), places=1)

        response = self.client.get(reverse('popular_view'))
        cars = response.json()

        # check that the response is sorted in desc. order of the key, 'rates_number'
        self.assert_(all(cars[i]['rates_number'] <= cars[max(i-1, 0)]['rates_number'] for i in range(len(cars))))
