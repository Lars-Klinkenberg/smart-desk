from controllers.height_controller import height_controller
from bottle import Bottle, request, HTTPResponse
import json

height_server = Bottle()


@height_server.post("/save")
def current_height():
    """
    calls db controller to save the height defined in the request header "height"

    Returns:
        string: serialized json either {"success": "..."} or {"error":"..."}
    """
    height = request.headers.get("height")

    if height is None:
        return HTTPResponse(status=400, body=json.dumps({"error": "height missing"}))
    try:
        height_controller.save_height(height)
        return json.dumps({"success": "saved height: " + height})
    except Exception as e:
        return HTTPResponse(status=500, body=json.dumps({"error": str(e)}))


@height_server.route("/current")
def current_height():
    """
    returns the last saved height (current height) from the db

    Returns:
        string: serialized json either {"height": num} or {"error": "..."}
    """
    return height_controller.get_current_height()


@height_server.route("/entries")
def get_todays_entries():
    """
    returns all entries of heights table either by day or all till limit is reached

    Request headers:
    day : "all" or the day ("yyyy-mm-dd")
    limit: only if day is set to all. how many entries should be returned (default: 15)

    Returns:
        string: serialized json either [data] or {"error" : "..."}
    """
    day = request.headers.get("day")
    limit = request.headers.get("limit")

    if limit is None:
        limit = 15

    if day == "all":
        return height_controller.get_all_heights(limit)

    return height_controller.get_all_entries_by_day(day)


@height_server.route("/total/day")
def get_total_time_of_day():
    """
    returns the calculated totals of given day

    Request headers:
    day: the day in the format "yyyy-mm-dd"

    Returns:
        string: serialized json either [data] or {"error" : "..."}
    """
    day = request.headers.get("day")

    return height_controller.get_totals_of_day(day)


@height_server.route("/total/today")
def get_todays_total_time():
    """
    returns the totals of the current day

    Returns:
        string: serialized json either [data] or {"error" : "..."}
    """
    return height_controller.get_todays_total()


@height_server.route("/total/yesterday")
def get_yesterdays_total_time():
    """
    returns the totals of yesterday

    Returns:
        string: serialized json either [data] or {"error" : "..."}
    """
    return height_controller.get_yesterdays_total()


@height_server.route("/total/year")
def get_total_times_of_year():
    """
    returns the totals of the given year

    Request headers:
    year: the year as an int

    Returns:
        string: serialized json either [data] or {"error" : "..."}
    """
    year = request.headers.get("year", None)
    if year is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "year header missing"})
        )

    return height_controller.get_daily_totals_of_year(year)
