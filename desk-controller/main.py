from serialService import SerialService
from converterService import ConverterService
from gpioService import GpioService
from deskController import DeskController


class Runntime:

    def __init__(self):
        self.serial = SerialService()
        self.gpio_service = GpioService()
        self.converter = ConverterService()
        self.desk = DeskController(self.serial)

    # closes all connections
    def stop(self):
        self.serial.close_connection()
        self.gpio_service.disable_write_to_serial()
        self.gpio_service.close()


rt = Runntime()

try:
    # rt.serial.activateDesk()
    rt.gpio_service.enable_write_to_serial()
    rt.desk.move_desk("UP")
#    print( rt.getCurrentHeight())

except KeyboardInterrupt:
    pass
finally:
    rt.stop()
