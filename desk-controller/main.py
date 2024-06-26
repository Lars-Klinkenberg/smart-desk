from serialService import SerialService
from converterService import ConverterService
from time import sleep
from gpioService import GpioService

class Runntime:
    # controller needs more than one short input to react
    # should work with about 15 iterations but sometimes it needs more to react. 
    WRITING_ITERATIONS = 50

    # Stop conditions
    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74
    
    def __init__(self):
        self.serial = SerialService()
        self.gpioService = GpioService()
        self.converter = ConverterService()
        
    # moves the desk to the given direction
    # TODO: detect if desk is not moving and handle it
    def moveDesk(self, direction):
        print("Moving desk to position: " + direction)
        
        self.gpioService.setRxOn()
        i = 0

        # send direction signal
        while i!= self.WRITING_ITERATIONS:
            i = i+1
            sleep(0.02)
            self.serial.writeStatus(direction)

        height = 0
        startedHeightAdjustment = False
        
        # write default while height is changing
        while (not self.maxHeightReached(height)) or not startedHeightAdjustment:
            self.serial.writeStatus("DEFAULT")
        
            # read current height data and iterate over chunks
            temp = self.converter.splitInValidChunks(self.serial.read())
            for t in temp:
                height = self.converter.convertHexArrToNumber(t)

                # only count valid heights                
                if height <= 0:
                    continue
                
                # if height is fist time not equal to sitting and standing height
                if (height != self.SITTING_HEIGHT) and (height != self.STANDING_HEIGHT):
                    startedHeightAdjustment = True
                    
                    
        print(f"Moved desk to height: {height}")
        self.gpioService.setRxOff()

    # closes all connections        
    def stop(self):
        self.serial.closeConnection()
        self.gpioService.setRxOff()
    
    # check if height is equal to sitting or standing height
    def maxHeightReached(self, height):
        if height == self.SITTING_HEIGHT:
            return True
        if height == self.STANDING_HEIGHT:
            return True
        
        return False
    
    # move the desk up or down depending on the current position
    def toggleDesk(self):
        # TODO: implement logic
        pass
        
    
rt = Runntime()

try:
    rt.moveDesk("DOWN")
except KeyboardInterrupt:
    pass
finally:
    rt.stop()