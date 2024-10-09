import signal
from threading import Event
import time
import logging
from utils.desk_state import desk_state
from controllers.desk_controller import desk_controller
from controllers.http_controller import http_controller

# Create a shutdown event to signal the loop to stop
shutdown_event = Event()


def get_current_height_loop():
    """
    Background thread to update the desk height
    """
    logger.info("Started loop with current height " + str(desk_state.get_height()))

    while not shutdown_event.is_set():
        try:
            time.sleep(0.5)
            desk_controller.measure_desk_height()

            if desk_controller.height_has_changed():
                http_controller.save_height(desk_state.get_height())
                desk_controller.reset_height_has_changed()
                logger.info("height has ben changed ...")
        except Exception as e:
            if (
                "returned no data (device disconnected or multiple access on port?)"
                in str(e)
            ):
                logger.warning(e)
            elif "Could not configure port: (5, 'Input/output error')" in str(e):
                logger.critical("No acces to serial port. shutting down ...")
                shutdown_event.set()
            else:
                logger.exception(f"exception while running get_current_height_loop")


def shutdown_handler(signum, frame):
    """
    Signal handler to gracefully shut down the loop.
    """
    logger.info("Received shutdown signal. Stopping the loop...")
    shutdown_event.set()  # Trigger the event to stop the loop


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="../logs/desk_controller.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        logger.info("starting desk_controller ...")
        desk_state.set_height(http_controller.get_current_height())
        get_current_height_loop()
    except Exception as e:
        logger.exception(f"Failed running main loop")
    finally:
        logger.info("Stopped desk_controller loop")
