import serial
from time import sleep


class SerialService:
    BAUD_RATE = 9600
    SERIAL_PORT = "/dev/ttyS0"

    HEX_STRING_PROFILE1 = "a50002fdff"
    HEX_STRING_PROFILE4 = "a50010efff"
    HEX_STRING_DEFAULT = "a50000ffff"

    HEX_STRING_UP = "a50020dfff"
    HEX_STRING_DOWN = "a50040bfff"

    def __init__(self):
        self.ser = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, serial.FIVEBITS)

    def read(self, timeout=None):
        """
        reads data from serial port and returns it

        Args:
            timeout (int, optional): set a timeout after which the serial reading gets interrupted. Defaults to None.

        Returns:
            bytes: serial as bytes
        """
        self.ser.timeout = timeout
        received_data = self.ser.read()  # read serial port
        sleep(0.03)
        data_left = self.ser.inWaiting()  # check for remaining byte
        received_data += self.ser.read(data_left)
        return received_data

    def write_hex_string_to_serial(self, hex_string):
        """
        takes a hex string array and writes it to the defined serial port
        """
        self.write(bytearray.fromhex(hex_string))

    # writes data to serial port
    def write_status(self, status):
        """
        writes the correct hex values matching the status

        Args:
            status (string): "UP" or "DOWN" or "DEFAULT"
        """
        if status == "UP":
            self.write_hex_string_to_serial(self.HEX_STRING_PROFILE1)
        elif status == "DOWN":
            self.write_hex_string_to_serial(self.HEX_STRING_PROFILE4)
        else:
            self.write_hex_string_to_serial(self.HEX_STRING_DEFAULT)

    def write(self, data):
        """
        writes the data to the serial port

        Args:
            data (bytes): data
        """

        self.ser.write(data)

    def close_connection(self):
        """
        closes the serial connetion
        """
        self.ser.close()


serial_service = SerialService()
