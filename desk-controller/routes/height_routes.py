from utils.desk_state import desk_state
from controllers.db_controller import db_controller
from bottle import Bottle, abort, response

height_server = Bottle()


@height_server.route('/current')
def current_height():
    return str(desk_state.get_height())

@height_server.route('/move')
def move_desk():
     abort(501)
     
@height_server.route('/entrys/<day>')
def get_todays_entrys(day):
    response.headers['Content-type'] = 'application/json'

    if day == "all":
        return db_controller.get_all_heights()
    
    return db_controller.get_all_entrys_by_day(day)
    