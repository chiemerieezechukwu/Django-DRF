import os
import django
import random
import requests
from api.external_api import get_models_for_make


base_url = "http://localhost:8000"


def add_entry_to_db(make, model):
    return requests.post(f"{base_url}/cars/", {"make": make, "model": model})


def get_all_entries():
    return requests.get(f"{base_url}/cars/")


def add_rating_to_entry(entry_id, rating):
    return requests.post(f"{base_url}/rate/", {"car_id": entry_id, "rating": rating})


make_name = "Volkswagen"
make_models = get_models_for_make(make=make_name)["Results"]


def populate():
    for model in make_models:
        res = add_entry_to_db(make=model["Make_Name"], model=model["Model_Name"])
        print(res.text, end=", ")
        print(res.status_code)


def rate_entry():
    for entry in get_all_entries().json():
        for _ in range(random.randint(10, 70)):
            res = add_rating_to_entry(entry_id=entry["id"], rating=random.randint(1, 5))
            print(res.text, end=", ")
            print(res.status_code)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crudproject.settings")
    django.setup()

    populate()
    rate_entry()
