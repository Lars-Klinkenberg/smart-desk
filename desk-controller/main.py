from serialService import SerialService
from converterService import ConverterService
from time import sleep

class Runntime:
    def start(self):
        print("STARTING RUNTIME")
        
        serial = SerialService()
        
        i=0
        # controller needs more than one short input to react
        # should work with about 15 iterations but sometimes it needs more to react. 
        while i!= 40:
            i = i+1
            sleep(0.02)
            serial.write("DOWN") 
            
        while True:
            serial.write("DEFAULT")
            sleep(0.03)

rt = Runntime()
rt.start()