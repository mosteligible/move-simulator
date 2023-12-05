from typing import Dict

from map_routes import map_utils
from map_routes.map_helpers import CurrentStretch
from shapely.geometry.point import Point

ROUTE_COORDINATES = [
    [-79.376727, 43.647003],
    [-79.375727, 43.647457],
    [-79.37525, 43.646337],
    [-79.375891, 43.646041],
    [-79.376375, 43.645844],
    [-79.37653, 43.645827],
    [-79.376539, 43.6457],
    [-79.37617, 43.644876],
    [-79.375904, 43.64422],
    [-79.37805, 43.64313],
    [-79.379217, 43.642511],
    [-79.379814, 43.642212],
    [-79.380306, 43.642127],
    [-79.381008, 43.641791],
]


class MockRouteHelper:
    last_position_index = 0


class MockRequest:
    def __init__(self, to_service: str, match: bool = True) -> None:
        self.to_service = to_service
        self.match = match

    def json(self) -> Dict:
        if self.to_service == "reverse-geocoder":
            if self.match:
                return [{"lat": 43.56789, "lon": -79.87654}]
            else:
                return []
        elif self.to_service == "routing-engine":
            if self.match:
                return {"points": {"coordinates": ROUTE_COORDINATES}}
            else:
                self.ok = False
                return []


def mocked_requests(to_service: str, match: bool) -> MockRequest:
    return MockRequest(to_service, match)


def test_postgis_point() -> None:
    coordinates = [[1, 2], [3, 4], [-5, 6]]
    expected_output = [Point([1, 2]), Point([3, 4]), Point([-5, 6])]
    for index, input in enumerate(coordinates):
        output = map_utils.postgis_point(input)
        assert isinstance(output, Point)
        assert output == expected_output[index]


def test_update_current_stretch() -> None:
    origin_coordinates = ROUTE_COORDINATES[0]
    destination_coordinates = ROUTE_COORDINATES[1]
    current_stretch = CurrentStretch(
        origin=origin_coordinates, destination=destination_coordinates
    )
    assert current_stretch == map_utils.update_current_stretch(
        current_stretch,
        current_stretch.distance - 1,  # distance covered is less than stretch length
        MockRouteHelper(),
        ROUTE_COORDINATES,
    )
    next_stretch = CurrentStretch(
        origin=ROUTE_COORDINATES[1], destination=ROUTE_COORDINATES[2]
    )
    assert next_stretch == map_utils.update_current_stretch(
        current_stretch,
        current_stretch.distance + 1,  # distance covered is more than stretch length
        MockRouteHelper(),
        ROUTE_COORDINATES,
    )
    assert next_stretch == map_utils.update_current_stretch(
        current_stretch,
        current_stretch.distance,  # when distance covered is equal to stretch length
        MockRouteHelper(),
        ROUTE_COORDINATES,
    )
