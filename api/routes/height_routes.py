from controllers.db_controller import db_controller
from bottle import Bottle, abort, response, request, HTTPResponse
import json

height_server = Bottle()


@height_server.post("/save")
def current_height():
    response.headers["Content-type"] = "application/json"
    height = request.headers.get("height")

    if height is None:
        return HTTPResponse(status=400, body=json.dumps({"error": "height missing"}))
    try:
        db_controller.save_height(height)
        return json.dumps({"success": "saved height: " + height})
    except Exception as e:
        return HTTPResponse(status=500, body=json.dumps({"error": str(e)}))


@height_server.route("/current")
def current_height():
    abort(501)


@height_server.route("/entrys")
def get_todays_entrys():
    response.headers["Content-type"] = "application/json"
    day = request.headers.get("day")
    limit = request.headers.get("limit")

    if limit is None:
        limit = 15

    if day == "all":
        return db_controller.get_all_heights(limit)

    return db_controller.get_all_entrys_by_day(day)
