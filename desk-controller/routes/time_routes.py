from bottle import Bottle, abort

time_server = Bottle()


@time_server.route('/avg')
def get_avg_standing_time():
    abort(501)

@time_server.route('/percentage')
def get_percentage_standing_time():
     abort(501)