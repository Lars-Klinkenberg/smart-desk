import os
import mariadb
from dotenv import load_dotenv
from datetime import datetime


class DatabaseController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
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
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute_query(self, query):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor

    def save_daily_total(self, day, height, time):
        save_query = "CALL saveDailyTotal('{}', {}, '{}')"

        try:
            print(save_query.format(day, height, time))
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(save_query.format(day, height, time))
            self.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

    def save_monthly_avg(self, height, time, id_of_month, year):
        save_query = "CALL saveMonthlyAvg({}, '{}', {}, {})"

        try:
            print(save_query.format(height, time, id_of_month, year))
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(save_query.format(height, time, id_of_month, year))
            self.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

    def get_totals_of_day(self, day):
        query = "CALL getTotalsOfDay('{}')"
        rows = []

        try:
            dayFormated = datetime.strptime(day, "%Y-%m-%d").date()

            cursor = self.execute_query(query.format(dayFormated))

            for total_time, height in cursor:
                rows.append({"total_time": str(total_time), "height": height})

        except ValueError:
            print("day not in valid format (yyyy-mm-dd)")
        except Exception as e:
            print("error: ", str(e))
        finally:
            self.close()
            return rows

    def get_daily_totals_entrys_of_day(self, day):
        query = "CALL getDailyTotalsEntrysOfDay('{}')"
        rows = []

        try:
            cursor = self.execute_query(query.format(day))

            for id, height, total_time, day in cursor:
                rows.append({"total_time": str(total_time), "height": height})

        except Exception as e:
            print("error: ", str(e))
        finally:
            self.close()
            return rows

    def get_monthly_avg_entrys_of_month(self, id_of_month, year):
        query = "CALL getMonthlyAvgEntrysOfMonth({}, {})"
        rows = []

        try:
            cursor = self.execute_query(query.format(id_of_month, year))

            for id, height, total_time, id_of_month, year in cursor:
                rows.append({"total_time": str(total_time), "height": height})

        except Exception as e:
            print("error: ", str(e))
        finally:
            self.close()
            return rows

    def get_month_avgs(self, id_of_month, year):
        query = "CALL getMonthAvgs({}, {})"
        rows = []

        try:
            cursor = self.execute_query(query.format(id_of_month, year))

            for height, avg_time in cursor:
                rows.append({"avg_time": str(avg_time), "height": height})

        except Exception as e:
            print("error: ", str(e))
        finally:
            self.close()
            return rows


db_controller = DatabaseController()
