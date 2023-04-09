# database update and local distance data updater
# Update latest distance data to database
# publish latest updated distance to subscribers

# update db every 10 seconds
# publish distance update data to subscriber every 1 second

import re
import requests
from typing import List, Tuple

from config import AppConfig
from message_queues.pubsub import DataSubscriber


def distance_stream(subscriber: DataSubscriber):
    """this could be any function that blocks until data is ready"""
    while True:
        yield f"data: {subscriber.receive_data()}\n\n"


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


def get_tuple_from_postgres_point(point: str) -> Tuple[float, float]:
    point = point.lower()
    point = re.sub(r"[point\(\)]", "", point)
    point = point.split(" ")
    return (float(point[0]), float(point[1]))


def get_route_coordinates(
    start_coordinate: str, stop_coordinate: str
) -> List:
    """
    start_coordinate: Tuple of float, float
        Has latitude and longitude coordinates as (latitude, longitude)
    start_coordinate: Tuple of float, float
        Has latitude and longitude coordinates as (latitude, longitude)
    """
    headers = {"Content-Type": "application/json"}
    start_coordinate = get_tuple_from_postgres_point(start_coordinate)
    stop_coordinate = get_tuple_from_postgres_point(stop_coordinate)
    query_parameters = {
        "profile": "car",
        "points": [
            [start_coordinate[1], start_coordinate[0]],
            [stop_coordinate[1], stop_coordinate[0]]
        ],
        "snap_preventions": ["ferry"],
        "details": ["road_class"],
        "locale": "en",
        "instructions": False,
        "calc_points": True,
        "points_encoded": False,
    }

    request_url = f"{AppConfig.routing_engine_endpoint}/route"
    response = requests.post(request_url, json=query_parameters, headers=headers)
    print("response:", response)
    if not response.ok:
        return False
    output = response.json()
    path = output['paths'][0]
    route_coordinates = path['points']
    return route_coordinates
