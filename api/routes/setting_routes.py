from bottle import Bottle, abort

setting_server = Bottle()


@setting_server.route('/standing/<height>')
def change_default_standing_height(height):
    abort(501)

@setting_server.route('/sitting/<height>')
def change_default_sitting_height(height):
     abort(501)