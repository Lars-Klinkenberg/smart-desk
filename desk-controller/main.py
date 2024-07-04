from Services.serialService import SerialService
from Services.converterService import ConverterService
from Services.gpioService import GpioService
from Services.deskService import DeskService
from Controller.heightController import HeightController

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

class Runntime:

    def __init__(self):
        self.serial = SerialService()
        self.gpio_service = GpioService()
        self.converter = ConverterService()
        self.desk = DeskService(self.serial)

    # closes all connections
    def stop(self):
        print("STOPPING")
        self.serial.close_connection()
        self.gpio_service.disable_write_to_serial()
        self.gpio_service.close()


if __name__ == "__main__":
    rt = Runntime()

    height_controller_arguments = {"gpio_service": rt.gpio_service, "desk": rt.desk}

    HeightController.register(
        app, route_base="/", init_argument=height_controller_arguments
    )
    app.run(debug=True, host='0.0.0.0')

    rt.stop()
