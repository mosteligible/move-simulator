import os

from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "backend")
        self.host_ip = os.getenv("HOST", "localhost")
        self.port = os.getenv("PORT", 5000)


class DatabaseConfig:
    def __init__(self) -> None:
        self.mysql_username = os.getenv("MYSQL_USERNAME", None)
        self.mysql_user_password = os.getenv("MYSQL_USER_PASSWORD", None)
        self.mysql_db_name = os.getenv("MYSQL_DB_NAME", None)
        self.mysql_user_table_name = os.getenv("MYSQL_USER_TABLE_NAME", None)
        self.mysql_route_table_name = os.getenv("MYSQL_ROUTE_TABLE_NAME", None)
        self.mysql_initdb_root_isername = os.getenv("MYSQL_INITDB_ROOT_USERNAME", None)
        self.mysqql_root_password = os.getenv("MYSQL_ROOT_PASSWORD", None)
        self.mysql_db_host = os.getenv("MYSQL_DB_HOST", None)
        self.mysql_db_port = os.getenv("MYSQL_DB_PORT", 3306)


AppConfig = ApplicationConfig()
DbConfig = DatabaseConfig()
