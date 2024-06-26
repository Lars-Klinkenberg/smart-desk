import RPi.GPIO as GPIO

class GpioService:
    PIN_RELAY = 26
    
    def __init__(self):
        GPIO.setmode (GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup (self.PIN_RELAY, GPIO.OUT)
        
    def setRxOff(self):
        GPIO.output(self.PIN_RELAY, False)
    
    def setRxOn(self):
        GPIO.output(self.PIN_RELAY, True)
        