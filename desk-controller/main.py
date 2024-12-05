import signal
from threading import Event
import time
from utils.desk_state import desk_state
from controllers.desk_controller import desk_controller
from controllers.http_controller import http_controller
from shared.logger import log

# Create a shutdown event to signal the loop to stop
shutdown_event = Event()


def get_current_height_loop():
    """
    Background thread to update the desk height
    """
    log("desk_controller", "INFO", "Started loop with current height " + str(desk_state.get_height()))

    while not shutdown_event.is_set():
        try:
            time.sleep(0.5)
            desk_controller.measure_desk_height()

            if desk_controller.height_has_changed():
                http_controller.save_height(desk_state.get_height())
                desk_controller.reset_height_has_changed()
                log("desk_controller", "INFO", "height has ben changed ...")
        except Exception as e:
            if (
                "returned no data (device disconnected or multiple access on port?)"
                in str(e)
            ):
                log("desk_controller", "WARNING", e)
            elif "Could not configure port: (5, 'Input/output error')" in str(e):
                log("desk_controller", "CRITICAL", "No acces to serial port. shutting down ...")
                shutdown_event.set()
            else:
                log("desk_controller", "ERROR", "exception while running get_current_height_loop")


def shutdown_handler(signum, frame):
    """
    Signal handler to gracefully shut down the loop.
    """
    log("desk_controller", "INFO", "Received shutdown signal. Stopping the loop...")
    shutdown_event.set()  # Trigger the event to stop the loop


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        log("desk_controller", "INFO", "starting desk_controller ...")
        desk_state.set_height(http_controller.get_current_height())
        get_current_height_loop()
    except Exception:
        log("desk_controller", "ERROR", "Failed running main loop")
    finally:
        log("desk_controller", "INFO", "Stopped desk_controller loop")
