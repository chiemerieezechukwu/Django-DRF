from django.urls import path
from .apis import CarDetailsAPI, CarRatingAPI, CarsAPI, PopularCars

urlpatterns = [
    path("cars/", CarsAPI.as_view(), name='cars_view'),
    path("cars/<int:car_id>/", CarDetailsAPI.as_view(), name='cars_details_view'),
    path("rate/", CarRatingAPI.as_view(), name='ratings_view'),
    path("popular/", PopularCars.as_view(), name='popular_view'),
]
