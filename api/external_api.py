import logging
import requests

BASE_API_ENDPOINT = "https://vpic.nhtsa.dot.gov/api/vehicles/"


def get_models_for_make(make):
    MODEL_FOR_MAKE_API = f"{BASE_API_ENDPOINT}GetModelsForMake/{make}?format=json"
    try:
        res = requests.get(MODEL_FOR_MAKE_API)
    except Exception as ex:
        logging.exception("Something went wrong: %s", str(ex))
        return None
    return res.json()
