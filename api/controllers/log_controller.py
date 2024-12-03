from controllers.db_controller import DatabaseController
import json
from datetime import datetime


class LogController(DatabaseController):
    """
    handles all the db calls related to logging
    """

    def save_log(self, service_name = None, level = None, message= None):
        """
        saves a log to the db
        
        Args:
            service_name (string): name of the service which called the log
            level (string): level of the log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message (string): log message

        Raises:
            ValueError: if an arg is not set
            RuntimeError: database error
        """
        SAVE_LOG_QUERY = "INSERT INTO logs (service_name, log_level, message) VALUES ('{}','{}','{}');"

        try:
            if(service_name is None) or (level is None) or (message is None):
                raise ValueError("Tried to save log but an argument was not found")
            
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(SAVE_LOG_QUERY.format(service_name, level, message.replace("'", "\\'")))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(e)
        finally:
            self.close()
            
    def get_all_logs(self, service_name, level):
        query = "SELECT * FROM logs WHERE service_name = '{}'"

        try:
            cursor = self.execute_query(query.format(service_name))
            rows = []

            for id, timestamp, service_name, log_level, message in cursor:
                rows.append(
                    {
                        "id": str(id),
                        "timestamp": str(timestamp),
                        "service_name": str(service_name),
                        "log_level": str(log_level),
                        "message": str(message),
                    }
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()
            
            
log_controller = LogController()