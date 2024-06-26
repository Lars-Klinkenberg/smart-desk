import serial
from time import sleep

BAUD_RATE = 9600
PORT = "/dev/ttyS0"

HEX_STRING_UP = "a50002fdff"
HEX_STRING_DOWN = "a50010efff"
HEX_STRING_EMPTY = "a50000ffff"

class SerialService:
    def __init__(self):
        self.ser = serial.Serial(PORT, BAUD_RATE)
    
    # reads data from serial port and returns it
    def read(self):
        received_data = self.ser.read()              #read serial port
        sleep(0.03)
        data_left = self.ser.inWaiting()             #check for remaining byte
        received_data += self.ser.read(data_left)
        return received_data
                
    def writeHexStringToSerial(self,hexString):
        self.write(bytearray.fromhex(hexString))
            
    # writes data to serial port
    def writeStatus(self,status):
        if status == "UP":
            self.writeHexStringToSerial(HEX_STRING_UP)
        elif status == "DOWN":
            self.writeHexStringToSerial(HEX_STRING_DOWN)
        else:
            self.writeHexStringToSerial(HEX_STRING_EMPTY)
    
    def write(self, data):
        self.ser.write(data)

    def closeConnection(self):
        self.ser.close()