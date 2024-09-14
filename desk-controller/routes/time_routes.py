from bottle import Bottle, abort, response
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
    response.headers['Content-type'] = 'application/json'
    return db_controller.get_todays_total(115)

@time_server.route('/yesterday')
def get_todays_total_time():
    response.headers['Content-type'] = 'application/json'
    return db_controller.get_yesterdays_total(115)

@time_server.route('/activity/<height>')
def get_daily_activity(height):
    response.headers['Content-type'] = 'application/json'
    return db_controller.get_daily_activity(height)