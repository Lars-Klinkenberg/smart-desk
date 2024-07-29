import os
import mariadb
from dotenv import load_dotenv


class DatabaseController:
    INSERT_HEIGHT_QUERRY = "INSERT INTO desk (height) VALUES ({});"
    GET_ALL_HEIGHTS_QUERRY = ""
    GET_TODAYS_TOTAL_TIME_QUERRY = ""
    GET_AVG_TOTAL_TIME_QUERRY = ""

    def __init__(self) -> None:
        load_dotenv()
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")

        if not self.user:
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
            print(f"Failed to connect to database {e}")

    def close(self):
        self.conn.close()

    def save_height(self, height):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(self.INSERT_HEIGHT_QUERRY.format(height))
        self.conn.commit()
        self.close()

        return


db_controller = DatabaseController()
