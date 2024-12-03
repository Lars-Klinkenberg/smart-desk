from bottle import Bottle
import bottle
from api.controllers.log_controller import log_controller
from routes.height_routes import height_server
from routes.setting_routes import setting_server
from routes.monitoring_routes import monitoring_server
from utils.enable_cors import EnableCors, add_cors_headers

mainApp = Bottle()


@mainApp.route("/<:re:.*>", method="OPTIONS")
def enable_cors_generic_route():
    """
    This route takes priority over all others. So any request with an OPTIONS
    method will be handled by this function.

    See: https://github.com/bottlepy/bottle/issues/402

    NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
    """
    add_cors_headers()


@mainApp.hook("after_request")
def enable_cors_after_request_hook():
    """
    This executes after every route. We use it to attach CORS headers when
    applicable.
    """
    add_cors_headers()

@mainApp.hook("before_request")
def log_request_call():
    log_controller.save_log("api", "INFO", f"recieved {bottle.request.method} on {bottle.request.fullpath}")

if __name__ == "__main__":

    try:
        log_controller.save_log("api", "INFO", "starting api ...")
        mainApp.mount("/height", height_server)
        mainApp.mount("/setting", setting_server)
        mainApp.mount("/monitoring", monitoring_server)

        # executes enable_cors on all routes (https://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests)
        mainApp.install(EnableCors())
        mainApp.run(host="0.0.0.0", port=8080)
    except Exception as e:
        log_controller.save_log("api", "ERROR", "Error while running main loop: ", e)
    finally:
        log_controller.save_log("api", "INFO", "Exited successfully")
