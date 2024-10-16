import os
import mariadb
from dotenv import load_dotenv
from datetime import datetime
import logging


class DatabaseController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = os.getenv("DB_NAME")
        self.logger = logging.getLogger(__name__)
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
            self.logger.exception("Failed to connect to database")
            self.conn = None

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute_query(self, query):
        self.connect()

        if not hasattr(self, "conn") or self.conn is None:
            self.logger.exception("Database connection is not established.")
            raise ConnectionError("Database connection is not established.")

        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor

    def save_daily_total(self, day, height, time):
        save_query = "CALL saveDailyTotal('{}', {}, '{}')"

        try:
            self.logger.info(
                f"saving daily total for: {day} at height {height} and time {time} "
            )
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(save_query.format(day, height, time))
            self.conn.commit()
        except Exception:
            self.logger.exception(f"failed to save daily total for day: {day}")
        finally:
            self.close()

    def save_monthly_avg(self, height, time, id_of_month, year):
        save_query = "CALL saveMonthlyAvg({}, '{}', {}, {})"

        try:
            self.logger.info(
                f"saving monthly avg for: {id_of_month}.{year} at height {height} and time {time} "
            )
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(save_query.format(height, time, id_of_month, year))
            self.conn.commit()
        except Exception:
            self.logger.exception(
                f"failed to save monthly avg for month: {id_of_month}, {year}"
            )
        finally:
            self.close()

    def get_totals_of_day(self, day):
        query = "CALL getTotalsOfDay('{}')"
        rows = []

        try:
            day_formated = datetime.strptime(day, "%Y-%m-%d").date()
            cursor = self.execute_query(query.format(day_formated))

            for total_time, height in cursor:
                if total_time is not None:
                    rows.append({"total_time": str(total_time), "height": height})

        except ValueError:
            self.logger.exception("day not in valid format (yyyy-mm-dd)")
        except Exception:
            self.logger.exception(f"failed while getting totals_of_day")
        finally:
            self.close()

        return rows

    def get_daily_totals_entries_of_day(self, day):
        query = "CALL getDailyTotalsEntriesOfDay('{}')"
        rows = []

        try:
            cursor = self.execute_query(query.format(day))

            for id, height, total_time, day in cursor:
                rows.append({"total_time": str(total_time), "height": height})

        except Exception:
            self.logger.exception(
                f"failed to load daily_totalss_entries_of_day for day {day}"
            )
        finally:
            self.close()

        return rows

    def get_monthly_avg_entries_of_month(self, id_of_month, year):
        query = "CALL getMonthlyAvgEntriesOfMonth({}, {})"
        rows = []

        try:
            cursor = self.execute_query(query.format(id_of_month, year))

            for id, height, total_time, id_of_month, year in cursor:
                rows.append({"total_time": str(total_time), "height": height})

        except Exception:
            self.logger.exception(
                f"failed to load monthly_avg_entries_of_month for month {id_of_month}, {year}"
            )
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

        except Exception:
            self.logger.exception(
                f"failed to load month_avgs for month {id_of_month}, {year}"
            )
        finally:
            self.close()

        return rows


db_controller = DatabaseController()
