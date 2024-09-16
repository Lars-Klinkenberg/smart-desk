import os
import mariadb
from dotenv import load_dotenv
import json


class DatabaseController:
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

    def execute_query(self, query):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor

    def save_height(self, height):
        query = "INSERT INTO desk (height) VALUES ({});"

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query.format(height))
            self.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

    def get_all_heights(self, limit):
        query = "SELECT height, time FROM desk ORDER BY time DESC LIMIT {};"

        try:
            cursor = self.execute_query(query.format(limit))
            rows = []

            for height, time in cursor:
                rows.append({"height": str(height), "time": str(time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_todays_total(self, height):
        query = "SELECT height, SUM(duration_seconds) AS total_duration_seconds FROM ( SELECT height, TIMESTAMPDIFF(SECOND, time, LEAD(time) OVER (ORDER BY time)) AS duration_seconds FROM desk WHERE DATE(time) = CURDATE()) AS durations WHERE height={} GROUP BY height;"

        try:
            cursor = self.execute_query(query.format(height))
            rows = []

            for height, total_duration_seconds in cursor:
                total_duration_minutes = round(total_duration_seconds / 60)
                rows.append(
                    {"height": height, "total_time": str(total_duration_minutes)}
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_all_entrys_by_day(self, day):
        query = "SELECT height, time FROM desk WHERE DATE(time) = '{}';"

        try:
            cursor = self.execute_query(query.format(day))
            rows = []

            for height, time in cursor:
                rows.append({"height": str(height), "time": str(time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_yesterdays_total(self, height):
        query = "SELECT height, SUM(duration_seconds) AS total_duration_seconds FROM ( SELECT height, TIMESTAMPDIFF(SECOND, time, LEAD(time) OVER (ORDER BY time)) AS duration_seconds FROM desk WHERE DATE(time) = CURDATE() - INTERVAL 1 DAY) AS durations WHERE height={} GROUP BY height;"

        try:
            cursor = self.execute_query(query.format(height))
            rows = []

            for height, total_duration_seconds in cursor:
                total_duration_minutes = round(total_duration_seconds / 60)
                rows.append(
                    {"height": height, "total_time": str(total_duration_minutes)}
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()


db_controller = DatabaseController()
