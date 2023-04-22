import re
import time
from threading import Thread
from typing import List

import requests
from config import AppConfig
from constants import DB_UPDATE_INTERVAL
from geoalchemy2.elements import WKBElement
from message_queues.pubsub import DataSubscriber
from models import db
from shapely.geometry import Point

from .map_helpers import CurrentStretch, RouteHelper
from .models import Route


def postgis_point(coordinate: List[float]) -> WKBElement:
    return Point(coordinate)


def update_distance_covered_in_route(route_proxy: RouteHelper, distance: float) -> None:
    from app import app

    with app.app_context():
        route = Route.query.filter_by(id=route_proxy.id).first()
        route.total_distance_covered += distance
        route.last_position_index = route_proxy.last_position_index + 1
        print(f">> updating route index: {route.last_position_index}")
        db.session.commit()
    return None


def update_current_stretch(
    current_stretch: CurrentStretch, route: RouteHelper, route_coordinates: List
) -> CurrentStretch:
    coordinate_index = route.last_position_index
    while True:
        if current_stretch.distance_covered >= current_stretch.distance:
            overshoot = current_stretch.distance_covered - current_stretch.distance
            coordinate_index += 1
            current_stretch = CurrentStretch(
                origin=route_coordinates[coordinate_index],
                destination=route_coordinates[coordinate_index + 1],
                distance_covered=overshoot,
            )
        else:
            return current_stretch


def update_current_stretch(
    current_stretch: CurrentStretch,
    distance_covered: float,
    route: RouteHelper,
    route_coordinates: List,
) -> CurrentStretch:
    """
    Update current stretch based on distance covered update from sensor.

    If distance covered data obtained from sensor is longer than length
    of current stretch, update current stretch's origin to next coordinate.
    If updated stretch's length is shorter than distance covered, update
    stretch again until length of sum of updated stretches is greater than
    or equal to distance covered data from sensor.
    """
    if current_stretch.distance_covered + distance_covered < current_stretch.distance:
        return current_stretch

    overshoot = (
        current_stretch.distance_covered + distance_covered - current_stretch.distance
    )
    stretch_distances = 0

    while stretch_distances - overshoot < 0:
        route.last_position_index += 1
        current_stretch = CurrentStretch(
            origin=route_coordinates[route.last_position_index],
            destination=route_coordinates[route.last_position_index + 1],
        )
        stretch_distances += current_stretch.distance

    return current_stretch


def distance_stream(subscriber: DataSubscriber, route: Route):
    """Received data and converts it to coordinate required for simulation"""
    route_proxy = RouteHelper(route=route)
    route_coordinates = route.route_coordinates["coordinates"]
    start_coordinate = route_coordinates[route_proxy.last_position_index]
    print(f"Route first two: {route_coordinates[:2]}")
    current_stretch = CurrentStretch(
        origin=start_coordinate,
        destination=route_coordinates[route_proxy.last_position_index + 1],
        distance_covered=0.0,
    )
    recent_db_update = time.perf_counter()
    distance_travelled_between_db_updates = 0
    while True:
        distance_data_from_sensor = subscriber.receive_data()
        distance_covered = float(distance_data_from_sensor) * 1000
        current_stretch.distance_covered += distance_covered
        distance_travelled_between_db_updates += distance_covered / 1000
        print(
            f"-- distance_covered: {distance_covered} current_stretch.distance: {current_stretch.distance}"
        )
        current_stretch = update_current_stretch(
            current_stretch=current_stretch,
            distance_covered=distance_covered,
            route=route_proxy,
            route_coordinates=route_coordinates,
        )
        next_coordinate = current_stretch.coordinate_from_origin_bearing_distance()
        print(
            f"origin: {current_stretch.origin}\n"
            f"next_coordinate: {next_coordinate}\n"
            f"destination: {current_stretch.destination}"
        )
        if time.perf_counter() - recent_db_update > DB_UPDATE_INTERVAL:
            distance_travelled_updater_thread = Thread(
                target=update_distance_covered_in_route,
                args=(route_proxy, distance_travelled_between_db_updates),
                daemon=True,
            )
            distance_travelled_updater_thread.start()
            recent_db_update = time.perf_counter()
            distance_travelled_between_db_updates = 0
        yield f"data: {next_coordinate}\n\n"


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
    return f"POINT({longitude} {latitude})"


def get_latlon_from_postgres_point(point: str) -> List[float]:
    point = point.lower()
    point = re.sub(r"[point\(\)]", "", point)
    point = point.split(" ")
    return [float(point[0]), float(point[1])]


def get_route_coordinates(start_coordinate: str, stop_coordinate: str) -> List:
    """
    start_coordinate: List of float, float
        Has latitude and longitude coordinates as (latitude, longitude)
    start_coordinate: List of float, float
        Has latitude and longitude coordinates as (latitude, longitude)
    """
    headers = {"Content-Type": "application/json"}
    start_coordinate = get_latlon_from_postgres_point(start_coordinate)
    stop_coordinate = get_latlon_from_postgres_point(stop_coordinate)
    query_parameters = {
        "profile": "car",
        "points": [
            start_coordinate,
            stop_coordinate,
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
    path = output["paths"][0]
    route_coordinates = path["points"]
    return route_coordinates
