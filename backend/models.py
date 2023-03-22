from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String())

    def __init__(self, id: str, username: str, email: str, password: str) -> None:
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
