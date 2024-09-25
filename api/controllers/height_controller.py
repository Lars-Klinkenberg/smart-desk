from controllers.db_controller import DatabaseController
import json
from datetime import datetime


class HeightController(DatabaseController):
    def save_height(self, height):
        SAVE_END_HEIGHT_QUERY = "CALL saveEndHeight({})"
        SAVE_START_HEIGHT_QUERY = "CALL saveStartHeight({})"

        try:
            if not self.validate_latest_entry(height):
                raise Exception("height or latest entry not valid")

            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(SAVE_END_HEIGHT_QUERY.format(height))
            self.conn.commit()
            cursor.execute(SAVE_START_HEIGHT_QUERY.format(height))
            self.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

    def get_all_heights(self, limit):
        query = "CALL getAllHeights({});"

        try:
            cursor = self.execute_query(query.format(limit))
            rows = []

            for id, start_time, start_height, end_time, end_height in cursor:
                rows.append(
                    {
                        "id": str(id),
                        "start_time": str(start_time),
                        "start_height": str(start_height),
                        "end_time": str(end_time),
                        "end_height": str(end_height),
                    }
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_todays_total(self):
        query = "CALL getTotalsOfDay(CURDATE());"

        try:
            cursor = self.execute_query(query)
            rows = []

            for total_time, height in cursor:
                rows.append({"height": height, "total_time": str(total_time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_all_entrys_by_day(self, day):
        query = "CALL getAllHeightsOfDay('{}');"

        try:
            dayFormated = datetime.strptime(day, "%Y-%m-%d").date()
            cursor = self.execute_query(query.format(dayFormated))
            rows = []

            for id, start_time, start_height, end_time, end_height in cursor:
                rows.append(
                    {
                        "id": str(id),
                        "start_time": str(start_time),
                        "start_height": str(start_height),
                        "end_time": str(end_time),
                        "end_height": str(end_height),
                    }
                )

            return json.dumps(rows)
        except ValueError:
            return json.dumps({"error": "day not in valid format (yyyy-mm-dd)"})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_yesterdays_total(self):
        query = "CALL getTotalsOfDay(CURDATE() - INTERVAL 1 DAY);"

        try:
            cursor = self.execute_query(query)
            rows = []

            for total_time, height in cursor:
                rows.append({"height": height, "total_time": str(total_time)})

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_totals_of_day(self, day):
        query = "CALL getTotalsOfDay('{}');"

        try:
            dayFormated = datetime.strptime(day, "%Y-%m-%d").date()
            print(query.format(dayFormated))
            cursor = self.execute_query(query.format(dayFormated))
            rows = []

            for total_time, height in cursor:
                rows.append({"height": height, "total_time": str(total_time)})

            return json.dumps(rows)
        except ValueError:
            return json.dumps({"error": "day not in valid format (yyyy-mm-dd)"})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def validate_latest_entry(self, newHeight) -> bool:
        query = "CALL getLatestHeight()"

        try:
            self.connect()
            cursor = self.execute_query(query)
            rows = []

            for id, start_time, start_height, end_time, end_height in cursor:
                rows.append(
                    {
                        "id": id,
                        "start_time": start_time,
                        "start_height": start_height,
                        "end_time": end_time,
                        "end_height": end_height,
                    }
                )

            if len(rows) > 1 or len(rows) == 0:
                raise Exception("getLatestHeight returned none unique result")

            latest_end_height = rows[0].get("end_height")
            if latest_end_height is not None:
                raise Exception(f"end_height of id:{rows[0].id} is already set")

            latest_start_height = str(rows[0].get("start_height"))

            if latest_start_height == newHeight:
                raise Exception(f"end_height of id:{rows[0].id} is equal to new height")

            return True
        except Exception as e:
            return False
        finally:
            self.close()

    def get_current_height(self):
        query = "CALL getLatestHeight();"

        try:
            cursor = self.execute_query(query)
            height = 0

            for id, start_time, start_height, end_time, end_height in cursor:
                print(start_height)
                height = start_height

            return json.dumps({"height": start_height})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_daily_totals_of_year(self, year):
        query = "CALL getDailyTotalsOfYear({});"

        try:
            cursor = self.execute_query(query.format(year))
            rows = []

            for id, height, total_time, day in cursor:
                rows.append(
                    {"height": height, "total_time": str(total_time), "day": str(day)}
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

height_controller = HeightController()