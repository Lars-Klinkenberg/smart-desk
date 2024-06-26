from serialService import SerialService
from converterService import ConverterService
from time import sleep
from gpioService import GpioService

class Runntime:
    def start(self):
        print("STARTING RUNTIME")
        
        serial = SerialService()
        gpioService = GpioService()
        converter = ConverterService()

        gpioService.setRxOn()
        i=0
        # controller needs more than one short input to react
        # should work with about 15 iterations but sometimes it needs more to react. 
        while i!= 40:
            i = i+1
            sleep(0.02)
            serial.writeStatus("DOWN")
        
        i = 0
        # TODO: end with height
        while i!= 100:
            serial.writeStatus("DEFAULT")
            print(converter.splitInValidChunks(serial.read()))
            sleep(0.03)
            i += 1
        gpioService.setRxOff()
        

rt = Runntime()
rt.start()