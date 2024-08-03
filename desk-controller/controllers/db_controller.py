import os
import mariadb
from dotenv import load_dotenv


class DatabaseController:
    INSERT_HEIGHT_QUERRY = "INSERT INTO desk (height) VALUES ({});"
    GET_ALL_HEIGHTS_QUERRY = "SELECT height FROM desk;"
    GET_TODAYS_TOTAL_TIME_QUERRY = ""
    GET_AVG_TOTAL_TIME_QUERRY = ""

    def __init__(self) -> None:
        load_dotenv()
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")

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
            print(f"Failed to connect to database {e}")

    def close(self):
        self.conn.close()

    def save_height(self, height):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_HEIGHT_QUERRY.format(height))
            self.conn.commit()
            return {"success": "Successfully saved height"}
        except Exception as e:
            return {"error": f"{e}"}
        finally:
            self.close()

    def get_all_heights(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(self.GET_ALL_HEIGHTS_QUERRY)
            rows = cursor.fetchall()

            # get nested list like [[1], [2] , ...] to flat list
            flat_list = [item for sublist in rows for item in sublist]
            return {"success": flat_list}
        except Exception as e:
            return {"error": f"{e}"}
        finally:
            self.close()


db_controller = DatabaseController()
