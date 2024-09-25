from bottle import Bottle, request, abort
from controllers.height_controller import height_controller

time_server = Bottle()


@time_server.route("/today")
def get_todays_total_time():
    return height_controller.get_todays_total()


@time_server.route("/yesterday")
def get_todays_total_time():
    return height_controller.get_yesterdays_total()

@time_server.route("/year")
def get_todays_total_time():
    year = request.headers.get("year", None)
    print(year)
    if year is None:
        abort(400)
    
    return height_controller.get_daily_totals_of_year(year)

@time_server.route("/day")
def get_todays_total_time():
    day = request.headers.get("day")

    return height_controller.get_totals_of_day(day)
