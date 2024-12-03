import json
from bottle import Bottle, request
from api.controllers.log_controller import log_controller
from api.utils.monitoring_service import is_service_active
from utils.enable_cors import add_cors_headers

monitoring_server = Bottle()


@monitoring_server.route("/<:re:.*>", method="OPTIONS")
def enable_cors_generic_route():
    """
    This route takes priority over all others. So any request with an OPTIONS
    method will be handled by this function.

    See: https://github.com/bottlepy/bottle/issues/402

    NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
    """
    add_cors_headers()


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


@monitoring_server.post("/logs/save_log")
def save_log():
    service_name = request.headers.get("service_name")
    level = request.headers.get("level")
    message = request.headers.get("message")
    
    log_controller.save_log(service_name, level, message)
    return json.dumps({"succes" : "saved log"})


@monitoring_server.route("/logs")
def get_api_logs():
    """
    returns the logs of a service

    Returns:
        string: serialized json
    """
    log_level = request.headers.get("level")
    service_name = request.headers.get("service_name")
    return log_controller.get_all_logs(service_name, log_level)