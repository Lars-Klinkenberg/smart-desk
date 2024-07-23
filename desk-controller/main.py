import signal
import sys
from flask import Flask
from threading import Thread, Event
import time
from routes.desk_routes import desk_bp
from utils.desk_state import desk_state

app = Flask(__name__)
app.register_blueprint(desk_bp, url_prefix="/api")

# Create a shutdown event to signal the background thread to stop
shutdown_event = Event()


def get_current_height_loop():
    while not shutdown_event.is_set():
        time.sleep(10)  # Change height every 10 seconds
        with app.app_context():  # Access the api context
            if not desk_state.is_moving:
                current_height = desk_state.get_height()
                new_height = (
                    current_height + 5 if current_height < 100 else 0
                )  # Example logic
                desk_state.set_height(new_height)
                print(f"Background thread updated height to {new_height}")


def change_desk_height_loop():
    while not shutdown_event.is_set():
        with app.app_context():
            pass


def signal_handler(sig, frame):
    shutdown_event.set()  # Signal the background thread to stop
    sys.exit(0)


def exit():
    print("-- Exited successfully --")
    pass


if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the background thread
    thread = Thread(target=get_current_height_loop)
    thread.start()

    # Run the Flask app
    try:
        app.run(debug=True)
    finally:
        shutdown_event.set()  # Signal the background thread to stop
        thread.join()  # Wait for the background thread to finish
        exit()
