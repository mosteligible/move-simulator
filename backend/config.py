import base64
import os
from hashlib import sha256
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv()


def not_set_error(var_name: str) -> None:
    raise ValueError(f"{var_name} is not set in environment!")


class ApplicationConfig:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "backend")
        self.host_ip = os.getenv("HOST", "localhost")
        self.port = os.getenv("PORT", 5000)
        self.reverse_geocoder_endpoint = os.getenv(
            "REVERSE_GEOCODER_ENDPOINT" ""
        )  # not_set_error("REVERSE_GEOCODER_ENDPOINT"))
        self.routing_engine_endpoint = os.getenv(
            "ROUTING_ENGINE_ENDPOINT" ""
        )  # not_set_error("ROUTING_ENGINE_ENDPOINT"))


class ConsumerConfig:
    def __init__(self) -> None:
        self.broker_host = os.getenv("BROKER_HOST", "")  # not_set_error("BROKER_HOST"))
        self.broker_port = os.getenv("BROKER_PORT", "")  # not_set_error("BROKER_PORT"))
        self.vhost = os.getenv("BROKER_VHOST", "")  # not_set_error("BROKER_VHOST"))
        self._username = os.getenv(
            "BROKER_USERNAME", ""
        )  # not_set_error("BROKER_USERNAME"))
        self._password = os.getenv(
            "BROKER_PASSWORD", ""
        )  # not_set_error("BROKER_PASSWORD"))
        self.credentials = pika.PlainCredentials(
            username=self._username, password=self._password
        )
        self.salt = os.getenv("SALT", None)  # not_set_error("SALT"))
        if self.salt is None:
            self.salt = os.urandom(4)
        else:
            self.salt = self.salt.encode("utf-8")

    def encode_password(self, password: str) -> str:
        password_encoded = password.encode("utf-8")
        salted_password = self.salt + password_encoded
        salted_sha256 = sha256(salted_password).digest()
        salted_hash_string = self.salt + salted_sha256
        password_hash = base64.b64encode(salted_hash_string)
        return password_hash.decode("utf-8")


class DatabaseConfig:
    def __init__(self) -> None:
        self.postgres_username = os.getenv(
            "PGRES_USERNAME", ""
        )  # not_set_error("PGRES_USERNAME"))
        self.postgres_user_password = os.getenv(
            "PGRES_USER_PASSWORD", ""
        )  # not_set_error("PGRES_USER_PASSWORD"))
        self.postgres_db_name = os.getenv(
            "POSTGRES_DB", ""
        )  # not_set_error("POSTGRES_DB"))
        self.postgres_user_table_name = os.getenv(
            "PGRES_USER_TABLE_NAME", ""
        )  # not_set_error("PGRES_USER_TABLE_NAME"))
        self.postgres_route_table_name = os.getenv(
            "PGRES_ROUTE_TABLE_NAME", ""
        )  # not_set_error("PGRES_ROUTE_TABLE_NAME"))
        self.postgres_initdb_root_username = os.getenv(
            "POSTGRES_USER", ""
        )  # not_set_error("POSTGRES_USER"))
        self.postgres_root_password = os.getenv(
            "POSTGRES_PASSWORD", ""
        )  # not_set_error("POSTGRES_PASSWORD"))
        self.postgres_db_host = os.getenv(
            "PGRES_DB_HOST", ""
        )  # not_set_error("PGRES_DB_HOST"))
        self.postgres_db_port = os.getenv("PGRES_DB_PORT", 3306)


AppConfig = ApplicationConfig()
DbConfig = DatabaseConfig()
brokerconfig = ConsumerConfig()
ROOT_DIR = Path(__file__).parent.absolute()
CONSUMER_LIST = {}
