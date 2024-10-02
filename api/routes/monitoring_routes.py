import json
import subprocess
import logging
from bottle import Bottle

monitoring_server = Bottle()


def is_service_active(service_name):
    logger = logging.getLogger(__name__)

    try:
        # Run the systemctl command to check if the service is active
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check the output; 'active' indicates the service is running
        return result.stdout.strip() == "active"

    except Exception as e:
        logger.error(f"Failed to load service ({service_name}) status: {e}")
        return False

    
def read_logs(path):
    logs = []
    try:
        with open(path, "r") as log_file:
            lines = log_file.readlines()

            for line in lines:
                args = line.split("|")

                if len(args) == 3:
                    logs.append(
                        {
                            "time": args[0].strip(),
                            "level": args[1].strip(),
                            "message": args[2].strip(),
                        }
                    )
    finally:
        return logs


@monitoring_server.route("/status")
def get_status():
    """
    returns status of services

    Returns:
        string: serialized json [{"service" : "status"}]
    """
    desk_controller_service_name = "desk-controller"
    api_controller_service_name = "api-controller"
    desk_controller_active = is_service_active(desk_controller_service_name)
    api_controller_active = is_service_active(api_controller_service_name)

    return json.dumps(
        {
            "api-controller": api_controller_active,
            "desk-controller": desk_controller_active,
        }
    )


@monitoring_server.route("/logs/api")
def get_controller_logs():
    """
    returns the logs of the api

    Returns:
        string: serialized json
    """
    return json.dumps(read_logs("../logs/api.log"))


@monitoring_server.route("/logs/controller")
def get_controller_logs():
    """
    returns the logs of the desk-controller

    Returns:
        string: serialized json
    """
    return json.dumps(read_logs("../logs/desk_controller.log"))


@monitoring_server.route("/logs/jobs/daily")
def get_controller_logs():
    """
    returns the logs of the daily job

    Returns:
        string: serialized json
    """
    return json.dumps(read_logs("../logs/calculate_daily_activity.log"))


@monitoring_server.route("/logs/jobs/monthly")
def get_controller_logs():
    """
    returns the logs of the monthly job

    Returns:
        string: serialized json
    """
    return json.dumps(read_logs("../logs/calculate_monthly_activity.log"))
