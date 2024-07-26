import RPi.GPIO as GPIO


class GpioService:
    PIN_RELAY = 26

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_RELAY, GPIO.OUT)

    def disable_write_to_serial(self):
        GPIO.output(self.PIN_RELAY, False)

    def enable_write_to_serial(self):
        GPIO.output(self.PIN_RELAY, True)

    def close(self):
        self.disable_write_to_serial()
        GPIO.cleanup()


# Create a global instance of the gpio service
gpio_service = GpioService()
