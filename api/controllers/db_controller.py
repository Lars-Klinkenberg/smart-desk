import os
import mariadb
from dotenv import load_dotenv
from api.controllers import log_controller


class DatabaseController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../../.env")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")
        self.conn = None

        if not self.user or not self.password or not self.host or not self.database:
            missing = [
                var
                for var, val in [
                    ("DB_USER", self.user),
                    ("DB_PASSWORD", self.password),
                    ("DB_HOST", self.host),
                    ("DB_NAME", self.database),
                ]
                if not val
            ]
            log_controller.save_log(
                "api", "ERROR", f"Missing database configuration: {', '.join(missing)}"
            )
            raise ValueError(f"Missing database configuration: {', '.join(missing)}")

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        except Exception:
            log_controller.save_log("api", "ERROR", "Failed to connect to database")
            self.conn = None

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute_query(self, query):
        self.connect()

        if not hasattr(self, "conn") or self.conn is None:
            log_controller.save_log(
                "api", "ERROR", "Database connection is not established."
            )
            raise ConnectionError("Database connection is not established.")

        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor
