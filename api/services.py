from django.http.response import Http404
from api.external_api import get_models_for_make
from .models import Car, CarRatings


def check_model_in_make(car_models: dict, model_name: str) -> bool:
    """
    car_models has the form
    {
        'Count': 0,
        'Message': 'Response returned successfully',
        'SearchCriteria': 'Make:NonExistent',
        'Results': [
            {
                'Make_ID': ...,
                'Make_Name': 'NonExistent',
                'Model_ID': ...,
                'Model_Name': ...
            }
        ]
    }
    """
    results = car_models["Results"]

    for value in results:
        if value["Model_Name"] == model_name:
            return True
    return False


def create_save_car_object(make, model):
    if retrieve_unique_car_by_filter(make, model):
        return "This car definition exists already", 403

    car_models = get_models_for_make(make)
    if car_models and check_model_in_make(car_models, model):
        car = Car(make=make, model=model)
        car.save()
        return car, 201
    return "The car's existence couldn't be verified", 400


def retrieve_unique_car_object_by_id(car_id):
    try:
        query = Car.objects.get(pk=int(car_id))
    except Car.DoesNotExist:
        raise Http404
    return query


def retrieve_unique_car_object_to_api(car_id):
    return retrieve_unique_car_object_by_id(car_id), 200


def retrieve_unique_car_by_filter(make, model):
    return Car.objects.filter(make=make, model=model).first()


def retrieve_cars_queryset():
    return Car.objects.all()


def retrieve_cars_queryset_order_desc(order_by):
    return retrieve_cars_queryset().order_by(f"-{order_by}")


def add_rating_to_car(car_id, rating):
    car = retrieve_unique_car_object_by_id(car_id)
    rate = CarRatings(car=car, rating=rating)
    rate.save()

    return f"Rating added to car with id {car_id}", 200


def delete_car_entry(car_id):
    car_to_delete = retrieve_unique_car_object_by_id(car_id)
    car_to_delete.delete()
    return f"Car with id {car_id} has been deleted succesfully", 204
