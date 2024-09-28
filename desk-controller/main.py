import signal
import sys
from threading import Thread, Event
import time
from utils.desk_state import desk_state
from utils.gpio_service import gpio_service
from controllers.desk_controller import desk_controller
from controllers.http_controller import http_controller

# Create a shutdown event to signal the background thread to stop
shutdown_event = Event()


def get_current_height_loop():
    """
    Background thread to update the desk height
    """

    print("Started loop with current height " + str(desk_state.get_height()))
    while not shutdown_event.is_set():
        try:
            time.sleep(0.5)  # Change height every 10 seconds
            desk_controller.measure_desk_height()

            if desk_controller.height_has_changed():
                http_controller.save_height(desk_state.get_height())
                desk_controller.reset_height_has_changed()
                print("height has ben changed ...")
        except Exception as e:
            print(f"Error in get_current_height_loop: {e}")


def shutdown_handler(signum, frame):
    """
    Signal handler to gracefully shut down the loop.
    """
    print("Received shutdown signal. Stopping the loop...")
    shutdown_event.set()  # Trigger the event to stop the loop


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        desk_state.set_height(http_controller.get_current_height())
        get_current_height_loop()
    except Exception as e:
        print(f"Error running loop: {e}")
    finally:
        print("Stopped")
