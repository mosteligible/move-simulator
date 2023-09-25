from geoalchemy2 import Geography
from models import db


class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    userid = db.Column(db.String(50), nullable=False)
    total_distance_covered = db.Column(db.Integer, nullable=False, default=0)
    last_position_index = db.Column(db.Integer, nullable=False, default=0)
    start_street_address = db.Column(db.String(250), nullable=False)
    start_city = db.Column(db.String(250), nullable=False)
    start_country = db.Column(db.String(50), nullable=False)
    end_street_address = db.Column(db.String(250), nullable=False)
    end_city = db.Column(db.String(250), nullable=False)
    end_country = db.Column(db.String(50), nullable=False)
    start_position = db.Column(Geography(geometry_type="POINT"), nullable=False)
    end_position = db.Column(Geography(geometry_type="POINT"), nullable=False)
    route_coordinates = db.Column(db.JSON, nullable=False)
    num_route_coordinates = db.Column(db.Integer, nullable=False)
