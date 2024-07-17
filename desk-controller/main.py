from time import sleep
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process, Value

from Services.serialService import SerialService
from Services.converterService import ConverterService
from Services.gpioService import GpioService
from Services.deskService import DeskService
from Controller.restController import RestController
from States.heightState import HeightState


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


class Runntime:

    def __init__(self):
        self.serial = SerialService()
        self.gpio_service = GpioService()
        self.converter = ConverterService()
        self.desk = DeskService(self.serial)
        self.heightState = HeightState(self.desk)

    # closes all connections
    def stop(self):
        self.serial.close_connection()
        self.gpio_service.disable_write_to_serial()
        self.gpio_service.close()

    def start(self):
        threads = []

        p = Process(target=self.loop)
        p.start()

        threads.append(p)
        self.initRestController()

        for t in threads:
            t.join()

        return threads

    def loop(self):
        while True:
            # check for height changes
            rt.heightState.readHeight()

    def initRestController(self):
        height_controller_arguments = {
            "gpio_service": rt.gpio_service,
            "desk": rt.desk,
        }

        RestController.register(
            app, route_base="/", init_argument=height_controller_arguments
        )
        app.run(debug=True, host="0.0.0.0", use_reloader=False)


if __name__ == "__main__":
    rt = Runntime()

    try:
        rt.start()
    except (KeyboardInterrupt, SystemExit):
        print("Received keyboard interrupt, quitting threads.")
    finally:
        rt.stop()
