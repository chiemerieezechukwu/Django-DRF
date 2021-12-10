import json
import random
from django.shortcuts import reverse
from django.test import TransactionTestCase
from api.models import Car


class TestCarsAPI(TransactionTestCase):

    reset_sequences = True
    
    def setUp(self):
        self.client.post(reverse('cars_view'), {
            'make': 'VOLKSWAGEN',
            'model': 'Golf'
        })

    def tearDown(self):
        Car.objects.all().delete()

    def test_car_entry_creation(self):
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

    def setUp(self):
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

    def setUp(self):
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
