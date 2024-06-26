from serialService import SerialService
from converterService import ConverterService
from time import sleep
from gpioService import GpioService

class Runntime:
    # controller needs more than one short input to react
    # should work with about 15 iterations but sometimes it needs more to react. 
    WRITING_ITERATIONS = 50
    def start(self):
        print("STARTING RUNTIME")
        
        serial = SerialService()
        gpioService = GpioService()
        converter = ConverterService()

        gpioService.setRxOn()
        i=0

        while i!= self.WRITING_ITERATIONS:
            i = i+1
            sleep(0.02)
            serial.writeStatus("DOWN")
        
        # write default while height is changing
        latestHeights = []
        while converter.isHeightChanging(latestHeights):
            serial.writeStatus("DEFAULT")
            temp = converter.splitInValidChunks(serial.read())
            for t in temp:
                height = converter.convertHexArrToNumber(t)
                if height != 0:
                    print(f"Current height: {height}")

                    latestHeights.append(height)
        print("FINISHED WRITING.")
        print(latestHeights)
        gpioService.setRxOff()
        

rt = Runntime()
rt.start()