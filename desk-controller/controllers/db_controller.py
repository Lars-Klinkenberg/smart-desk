import os
import mariadb
from dotenv import load_dotenv
import json

class DatabaseController:
    INSERT_HEIGHT_QUERRY = "INSERT INTO desk (height) VALUES ({});"
    GET_ALL_ENTRYS_QUERRY = "SELECT height, time FROM desk;"
    GET_ALL_ENTRYS_OF_DAY_QUERRY = "SELECT height, time FROM desk WHERE DATE(time) = '{}';"
    GET_AVG_TOTAL_TIME_QUERRY = "SELECT height, AVG(total_duration_seconds) AS avg_daily_duration_seconds FROM (SELECT height, date, SUM(duration_seconds) AS total_duration_seconds FROM (SELECT height, DATE(time) AS date, TIMESTAMPDIFF(SECOND, time, COALESCE(LEAD(time) OVER (PARTITION BY DATE(time) ORDER BY time), DATE_ADD(DATE(time), INTERVAL 1 DAY))) AS duration_seconds FROM desk) AS daily_durations GROUP BY height, date) AS daily_totals GROUP BY height;"
    GET_SPECIFIC_AVG_TOTAL_TIME_QUERRY = "SELECT AVG(total_duration_seconds) AS avg_daily_duration_seconds FROM (SELECT height, date, SUM(duration_seconds) AS total_duration_seconds FROM (SELECT height, DATE(time) AS date, TIMESTAMPDIFF(SECOND, time, COALESCE(LEAD(time) OVER (PARTITION BY DATE(time) ORDER BY time), DATE_ADD(DATE(time), INTERVAL 1 DAY))) AS duration_seconds FROM desk) AS daily_durations GROUP BY height, date) AS daily_totals WHERE height={} GROUP BY height;"
    GET_TOTAL_TIMES_QUERRY = "SELECT height, SUM(duration_seconds) AS total_duration_seconds FROM ( SELECT height, TIMESTAMPDIFF(SECOND, time, LEAD(time) OVER (ORDER BY time)) AS duration_seconds FROM desk) AS durations GROUP BY height;"
    GET_ACTIVITY_QUERRY = "WITH desk_with_lead AS (SELECT id, height, time,LEAD(time) OVER (ORDER BY time) AS next_time FROM desk) SELECT DATE(time) AS day, height, SEC_TO_TIME(SUM(TIMESTAMPDIFF(SECOND, time, COALESCE(next_time, NOW())))) AS total_time FROM desk_with_lead WHERE height={} GROUP BY day, height ORDER BY day;"
    
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
        except Exception as e:
           raise Exception(e)
        finally:
            self.close()

    def get_all_heights(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(self.GET_ALL_ENTRYS_QUERRY)
            rows = []

            for(height, time) in cursor:
                rows.append({"height": str(height), "time" : str(time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()
            
    def get_todays_total(self, height):
        query = "SELECT height, SUM(duration_seconds) AS total_duration_seconds FROM ( SELECT height, TIMESTAMPDIFF(SECOND, time, LEAD(time) OVER (ORDER BY time)) AS duration_seconds FROM desk WHERE DATE(time) = CURDATE()) AS durations WHERE height={} GROUP BY height;"
        
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query.format(height))
            rows = []

            for (height, total_duration_seconds) in cursor:
                total_duration_minutes = round(total_duration_seconds / 60)
                rows.append({"height" : height, "total_time" : str(total_duration_minutes)})
            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()
    
    def get_all_entrys_by_day(self,day):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(self.GET_ALL_ENTRYS_OF_DAY_QUERRY.format(day))
            rows = []

            for(height, time) in cursor:
                rows.append({"height": str(height), "time" : str(time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_daily_activity(self, height):
        try:
            self.connect()
            cursor = self.conn.cursor()
            print(self.GET_ALL_ENTRYS_QUERRY.format(height))
            cursor.execute(self.GET_ACTIVITY_QUERRY.format(height))
            rows = []
            
            for(day, height, total_time) in cursor:
                rows.append({"day": str(day), "total_time" : str(total_time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()
            
    def get_yesterdays_total(self, height):
        query = "SELECT height, SUM(duration_seconds) AS total_duration_seconds FROM ( SELECT height, TIMESTAMPDIFF(SECOND, time, LEAD(time) OVER (ORDER BY time)) AS duration_seconds FROM desk WHERE DATE(time) = CURDATE() - INTERVAL 1 DAY) AS durations WHERE height={} GROUP BY height;"

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query.format(height))
            rows = []

            for (height, total_duration_seconds) in cursor:
                total_duration_minutes = round(total_duration_seconds / 60)
                rows.append({"height" : height, "total_time" : str(total_duration_minutes)})
            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()
db_controller = DatabaseController()
