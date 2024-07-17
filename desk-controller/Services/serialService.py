import serial
from time import sleep

BAUD_RATE = 9600
PORT = "/dev/ttyS0"

HEX_STRING_PROFILE1 = "a50002fdff"
HEX_STRING_PROFILE4 = "a50010efff"
HEX_STRING_DEFAULT = "a50000ffff"

HEX_STRING_UP = "a50020dfff"
HEX_STRING_DOWN = "a50040bfff"


class SerialService:
    def __init__(self):
        self.ser = serial.Serial(PORT, BAUD_RATE, serial.FIVEBITS)

    # reads data from serial port and returns it
    def read(self, timeout = None):
        received_data = self.ser.read()  # read serial port
        sleep(0.03)
        data_left = self.ser.inWaiting()  # check for remaining byte
        received_data += self.ser.read(data_left)
        return received_data

    def write_hex_string_to_serial(self, hex_string):
        self.write(bytearray.fromhex(hex_string))

    # writes data to serial port
    def write_status(self, status):
        if status == "UP":
            self.write_hex_string_to_serial(HEX_STRING_PROFILE1)
        elif status == "DOWN":
            self.write_hex_string_to_serial(HEX_STRING_PROFILE4)
        else:
            self.write_hex_string_to_serial(HEX_STRING_DEFAULT)

    def write(self, data):
        self.ser.write(data)

    def close_connection(self):
        self.ser.close()

    def activateDesk(self):
        self.write_hex_string_to_serial(HEX_STRING_UP)
        self.write_hex_string_to_serial(HEX_STRING_UP)
        sleep(1)
        self.write_hex_string_to_serial(HEX_STRING_DOWN)
        self.write_hex_string_to_serial(HEX_STRING_DOWN)