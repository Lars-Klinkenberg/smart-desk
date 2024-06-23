from serialService import SerialService
from converterService import ConverterService
from time import sleep

class Runntime:
    def start(self):
        print("STARTING RUNTIME")
        
        serial = SerialService()
        
        i=0
        # controller needs more than one short input to react
        # should work with about 15 iterations
        while i!= 20:
            i = i+1
            # TODO check if it works better with higher delays  
            sleep(0.03)
            serial.write("DOWN") 
            
        while True:
            serial.write("DEFAULT")
            sleep(0.03)

rt = Runntime()
rt.start()