from utils.desk_state import desk_state
from bottle import Bottle, abort

height_server = Bottle()


@height_server.route('/current')
def current_height():
    return str(desk_state.get_height())

@height_server.route('/move')
def move_desk():
     abort(501)