from controllers.db_controller import db_controller
from bottle import Bottle, abort, response
import json

height_server = Bottle()

@height_server.route('/save/<height>')
def current_height(height):
    try:
        db_controller.save_height(height)
        return json.dumps({"success": "saved height :" + height})
    except Exception as e:
        return json.dumps({"error": str(e)})

@height_server.route('/current')
def current_height():
    abort(501)


@height_server.route('/move')
def move_desk():
     abort(501)
     
@height_server.route('/entrys/<day>')
def get_todays_entrys(day):
    response.headers['Content-type'] = 'application/json'

    if day == "all":
        return db_controller.get_all_heights(15)
    
    return db_controller.get_all_entrys_by_day(day)
    