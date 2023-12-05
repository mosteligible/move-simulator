import time
from dataclasses import dataclass
from threading import Lock
from typing import List

import constants
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic

from .models import Route, db


@dataclass
class Position:
    street_address: str
    coordinates: List[float]


class CurrentStretch:
    def __init__(
        self,
        origin: List[float],
        destination: List[float],
        distance_covered: float = 0.0,
    ) -> None:
        self.origin = origin
        self.destination = destination
        self.distance, self.bearing = self.dist_bearing_between_points(
            self.origin, self.destination
        )
        self.distance_covered = distance_covered

    @staticmethod
    def dist_bearing_between_points(
        coord1: List[float], coord2: List[float]
    ) -> List[float]:
        """
        Get bearing angle between two lat-lon coordinates:

        :params:
            coord1: List of floats.
                    Contains two elements in order (latitude, longitude)
            coord1: List of floats.
                    Contains two elements in order (latitude, longitude)
        """
        dist_bearing_angle = Geodesic.WGS84.Inverse(*coord1, *coord2)
        distance = dist_bearing_angle["s12"]
        bearing_angle = dist_bearing_angle["azi1"]
        return distance, bearing_angle

    def coordinate_from_origin_bearing_distance(self) -> List[float]:
        """
        From start lat-lon coordinates, gets lat-lon  coordinate at `distance` that is at `bearing` angle.

        :params:
            origin: List of length two, contains two floating point numbers.
                    Two floating point numbers represent latitude and longitude in degrees.
            bearing: Angle (in degrees) from origin to the destination point.
            distance: Distance between origin and destination point (in meters).

        returns: List of two floaring point numbers.
                Each number represents latitude and longitude of destination in degrees.
        """
        geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
        destination = geod.Direct(*self.origin, self.bearing, self.distance_covered)
        return [destination["lat2"], destination["lon2"]]

    def __eq__(self, other: "CurrentStretch") -> bool:
        """
        Two stretches are equal if their origin and destination are same.
        """
        origin_equal = all(x == y for x, y in zip(self.origin, other.origin))
        destination_equal = all(
            x == y for x, y in zip(self.destination, other.destination)
        )
        return origin_equal and destination_equal

    def __repr__(self) -> str:
        origin = f"POINT({self.origin[1]}, {self.origin[0]})"
        destination = f"POINT({self.destination[1]}, {self.destination[0]})"
        return f"{origin} -> {destination}"


class RouteHelper:
    def __init__(self, route: Route) -> None:
        self.start_position = self.lat_lon_from_postgis_point(route.start_position)
        self.end_position = self.lat_lon_from_postgis_point(route.end_position)
        self.last_position_index = route.last_position_index
        self.last_position = route.route_coordinates[self.last_position_index]
        self.id = route.id
        self.start_street_address = route.start_street_address
        self.start_city = route.start_city
        self.end_street_address = route.end_street_address
        self.end_city = route.end_city

    @staticmethod
    def lat_lon_from_postgis_point(element: WKBElement) -> List[float]:
        point = to_shape(element)
        return [point.x, point.y]

    def decode_to_coordinates(self) -> None:
        self.encoded = False
        self.start_position = self.lat_lon_from_postgis_point(self.start_position)
        self.end_position = self.lat_lon_from_postgis_point(self.end_position)
        self.last_position = self.lat_lon_from_postgis_point(self.last_position)


class PositionUpdater:
    __lock = Lock()
    last_update_at: int

    def __init__(self, distnace_travelled: float = 0.0) -> None:
        self.last_update_at = time.time()
        self.distance_travelled = distnace_travelled

    def update_distance_covered(
        self, route_helper: RouteHelper, distance: float
    ) -> bool:
        with self.__lock:
            if time.time() - self.last_update_at < constants.DB_UPDATE_INTERVAL:
                return False
            from app import app

            with app.app_context():
                route: Route = Route.query.filter_by(id=route_helper.id).first()
                route.total_distance_covered += distance
                route.last_position_index = route_helper.last_position_index
                db.session.commit()
            self.last_update_at = time.time()

        return True
