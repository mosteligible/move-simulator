from models import db


class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.String(50), primary_key=True)
    device_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey("users.username"), nullable=False)
