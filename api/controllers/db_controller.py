import os
import mariadb
from dotenv import load_dotenv
import logging


class DatabaseController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")
        self.conn = None
        self.logger = logging.getLogger(__name__)

        if not self.user or not self.password or not self.host or not self.database:
            raise ValueError("Database configuration not found")

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        except Exception as e:
            self.loggger.error(f"Failed to connect to database {e}")

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute_query(self, query):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor
