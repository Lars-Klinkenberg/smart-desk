import signal
import sys
from flask import Flask
from threading import Thread, Event
import time
from routes.desk_routes import desk_bp
from utils.desk_state import desk_state
from utils.gpio_service import gpio_service
from controllers.db_controller import db_controller
from controllers.desk_controller import desk_controller

app = Flask(__name__)
app.register_blueprint(desk_bp, url_prefix="/api")

# Create a shutdown event to signal the background thread to stop
shutdown_event = Event()


def exit():
    """
    Clean up and exit the application
    """
    gpio_service.close()
    print("Exited successfully")
    pass


def get_current_height_loop():
    """
    Background thread to update the desk height
    """

    print("Started current height loop")
    print("To get the latest state of the Desk please press the move up/down button")
    while not shutdown_event.is_set():
        try:
            time.sleep(1)  # Change height every 10 seconds
            with app.app_context():  # Access the api context
                desk_controller.measure_desk_height()

                if desk_controller.height_has_changed():
                    db_controller.save_height(desk_state.get_height())
                    desk_controller.reset_height_has_changed()
        except Exception as e:  
            print(f"Error in get_current_height_loop: {e}")


def change_desk_height_loop():
    """
    Background thread to change the desk height
    """
    print("Started change height loop")
    while not shutdown_event.is_set():
        try:
            with app.app_context():
                time.sleep(5)
                if desk_state.should_desk_be_moved():
                    print("moving desk ...")
                    desk_controller.move(desk_state.get_moving_direction())
        except Exception as e:
            print(f"Error in change_desk_height_loop: {e}")


def signal_handler(sig, frame):
    """
    Signal handler for graceful shutdown
    """
    print("Exiting ....")
    shutdown_event.set()  # Signal the background thread to stop
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the background thread
    height_thread = Thread(target=get_current_height_loop)
    height_thread.start()

    change_thread = Thread(target=change_desk_height_loop)
    change_thread.start()

    # Run the Flask app
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error in main block: {e}") 
    finally:
        shutdown_event.set()  # Signal the background thread to stop
        height_thread.join()  # Wait for the background thread to finish
        change_thread.join()
        exit()
