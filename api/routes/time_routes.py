from bottle import Bottle, request
from controllers.db_controller import db_controller

time_server = Bottle()


@time_server.route("/today")
def get_todays_total_time():
    return db_controller.get_todays_total()


@time_server.route("/yesterday")
def get_todays_total_time():
    return db_controller.get_yesterdays_total()


@time_server.route("/day")
def get_todays_total_time():
    day = request.headers.get("day")

    return db_controller.get_totals_of_day(day)
