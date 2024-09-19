from bottle import Bottle, request, abort
from controllers.db_controller import db_controller

time_server = Bottle()


@time_server.route("/today")
def get_todays_total_time():
    return db_controller.get_todays_total()


@time_server.route("/yesterday")
def get_todays_total_time():
    return db_controller.get_yesterdays_total()

@time_server.route("/year")
def get_todays_total_time():
    year = request.headers.get("year", None)
    print(year)
    if year is None:
        abort(400)
    
    return db_controller.get_daily_totals_of_year(year)

@time_server.route("/day")
def get_todays_total_time():
    day = request.headers.get("day")

    return db_controller.get_totals_of_day(day)
