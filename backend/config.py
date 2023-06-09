import os
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "backend")
        self.host_ip = os.getenv("HOST", "localhost")
        self.port = os.getenv("PORT", 5000)
        self.reverse_geocoder_endpoint = os.getenv("REVERSE_GEOCODER_ENDPOINT", "")
        self.routing_engine_endpoint = os.getenv("ROUTING_ENGINE_ENDPOINT", "")


class ConsumerConfig:
    def __init__(self) -> None:
        self.broker_host = os.getenv("BROKER_HOST")
        self.broker_port = os.getenv("BROKER_PORT")
        self.vhost = os.getenv("BROKER_VHOST")
        self._username = os.getenv("BROKER_USERNAME")
        self._password = os.getenv("BROKER_PASSWORD")
        self.credentials = pika.PlainCredentials(
            username=self._username, password=self._password
        )


class DatabaseConfig:
    def __init__(self) -> None:
        self.postgres_username = os.getenv("PGRES_USERNAME", None)
        self.postgres_user_password = os.getenv("PGRES_USER_PASSWORD", None)
        self.postgres_db_name = os.getenv("POSTGRES_DB", None)
        self.postgres_user_table_name = os.getenv("PGRES_USER_TABLE_NAME", None)
        self.postgres_route_table_name = os.getenv("PGRES_ROUTE_TABLE_NAME", None)
        self.postgres_initdb_root_username = os.getenv("POSTGRES_USER", None)
        self.postgres_root_password = os.getenv("POSTGRES_PASSWORD", None)
        self.postgres_db_host = os.getenv("PGRES_DB_HOST", None)
        self.postgres_db_port = os.getenv("PGRES_DB_PORT", 3306)


AppConfig = ApplicationConfig()
DbConfig = DatabaseConfig()
brokerconfig = ConsumerConfig()
ROOT_DIR = Path(__file__).parent.absolute()
