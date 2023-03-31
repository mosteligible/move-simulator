import secrets
import time
from hashlib import sha256
from random import random

import requests
from config import AppConfig
from message_queues.pubsub import DataPublisher


def secret_key() -> str:
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key


def get_coordinates_from_address(
    street_address: str, city_name: str, country_name: str, postal_code: str = ""
) -> str:
    parameters = {"street": street_address, "city": city_name, "country": country_name}
    if postal_code != "":
        parameters["postalcode"] = postal_code

    url = f"{AppConfig.reverse_geocoder_endpoint}/search"

    response = requests.get(
        url,
        params=parameters,
    )
    reverse_geocodes = response.json()
    if len(reverse_geocodes) > 0:
        reverse_geocodes = reverse_geocodes[0]
        latitude = reverse_geocodes["lat"]
        longitude = reverse_geocodes["lon"]
    else:
        return False
    return f"POINT({latitude} {longitude})"
