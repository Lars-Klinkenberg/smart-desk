from bottle import Bottle, abort
from controllers.db_controller import db_controller
time_server = Bottle()


@time_server.route('/avg')
def get_avg_standing_time():
    abort(501)

@time_server.route('/percentage')
def get_percentage_standing_time():
     abort(501)
     
@time_server.route('/today')
def get_todays_total_time():
    return db_controller.get_todays_total()

