import RPi.GPIO as GPIO


class GpioService:
    PIN_RELAY = 26

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_RELAY, GPIO.OUT)

    def set_rx_off(self):
        GPIO.output(self.PIN_RELAY, False)

    def set_rx_on(self):
        GPIO.output(self.PIN_RELAY, True)
