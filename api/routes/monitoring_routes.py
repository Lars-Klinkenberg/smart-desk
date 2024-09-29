import json
from bottle import Bottle, HTTPResponse, request

monitoring_server = Bottle()


@monitoring_server.route("/status")
def get_status():
    """
    returns status of services

    Returns:
        string: serialized json [{"service" : "status"}]
    """

    return json.dumps([{"api": "up"}])


@monitoring_server.route("/logs/api")
def get_controller_logs():
    """
    returns the logs of the api

    Returns:
        string: serialized json
    """
    logs = []
    with open("../logs/api.log", "r") as log_file:
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

    return json.dumps(logs)


@monitoring_server.route("/logs/controller")
def get_controller_logs():
    """
    returns the logs of the desk-controller

    Returns:
        string: serialized json
    """
    logs = []
    with open("../logs/desk_controller.log", "r") as log_file:
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

    return json.dumps(logs)
