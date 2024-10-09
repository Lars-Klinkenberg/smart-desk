from controllers.db_controller import DatabaseController
import json
from datetime import datetime


class HeightController(DatabaseController):
    """
    handles all the db calls related to the height
    """

    def save_height(self, height):
        """
        validates the height and saves it to the db if valid

        Args:
            height (int): new height to be saved

        Raises:
            ValueError: if height is not valid
            RuntimeError: database error
        """
        SAVE_END_HEIGHT_QUERY = "CALL saveEndHeight({})"
        SAVE_START_HEIGHT_QUERY = "CALL saveStartHeight({})"

        try:
            if not self.validate_latest_entry(height):
                raise ValueError("height or latest entry not valid")

            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(SAVE_END_HEIGHT_QUERY.format(height))
            self.conn.commit()
            cursor.execute(SAVE_START_HEIGHT_QUERY.format(height))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(e)
        finally:
            self.close()

    def get_all_heights(self, limit):
        """
        get all heights entrys of current day

        Args:
            limit (int): limits how many entrys should be returned

        Returns:
            string: serialized json either [{id, start_time, start_height, end_time, end_height}] or {"error" : "..."}
        """
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
        """
        returns the calculated totals of the current day

        Returns:
            string: serialized json either [{height, total_time}] or {"error" : "..."}
        """
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
        """
        returns the heights entrys of given day

        Args:
            day (string): day in the format yyyy-mm-dd

        Returns:
            string: serialized json either [{id, start_time, start_height, end_time, end_height}] or {"error" : "..."}
        """
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
        """
        get the totaly of yesterday

        Returns:
            string: serialized json either [{height, total_time}] or {"error" : "..."}
        """
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
        """
        returns the calculated totals of given day

        Args:
            day (string): the day in the format yyyy-mm-dd

        Returns:
            string: serialized json either [{height, total_time}] or {"error" : "..."}
        """
        query = "CALL getTotalsOfDay('{}');"

        try:
            dayFormated = datetime.strptime(day, "%Y-%m-%d").date()
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
        """
        checks if a height can be saved to the db

        Args:
            newHeight (int): height that should be saved

        Raises:
            Exception: if height is not valid


        Returns:
            bool: true if height can be saved
        """
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
            raise Exception(e) from e
        finally:
            self.close()

    def get_current_height(self):
        """
        returns the latest height

        Returns:
            string: serialized json either {"height" : num} or {"error" : "..."}
        """
        query = "CALL getLatestHeight();"

        try:
            cursor = self.execute_query(query)
            height = 0

            for id, start_time, start_height, end_time, end_height in cursor:
                if end_height == None:
                    height = start_height
                else:
                    height = end_height

            return json.dumps({"height": height})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_daily_totals_of_year(self, year):
        """
        returns the total of each day of the given year

        Args:
            year (int): year in the format yyyy

        Returns:
            string: serialized json either [{height, total_time}] or {"error" : "..."}
        """
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
