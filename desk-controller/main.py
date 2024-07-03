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
        self.gpio_service = GpioService()
        self.converter = ConverterService()

    # moves the desk to the given direction
    # TODO: detect if desk is not moving and handle it
    def move_desk(self, direction):
        print("Moving desk to position: " + direction)

        self.gpio_service.enable_write_to_serial()
        i = 0
        # send direction signal
        while i != self.WRITING_ITERATIONS:
            i = i + 1
            sleep(0.02)
            self.serial.write_status(direction)

        height = 0
        started_height_adjustment = False

        # write default while height is changing
        while (not self.max_height_reached(height)) or not started_height_adjustment:
            self.serial.write_status("DEFAULT")

            # read current height data and iterate over chunks
            for t in self.getDeskHeight():
                # if height is fist time not equal to sitting and standing height
                if (height != self.SITTING_HEIGHT) and (height != self.STANDING_HEIGHT):
                    started_height_adjustment = True

        print(f"Moved desk to height: {height}")
        self.gpio_service.disable_write_to_serial()

    # closes all connections
    def stop(self):
        self.serial.close_connection()
        self.gpio_service.disable_write_to_serial()
        self.gpio_service.close()

    # check if height is equal to sitting or standing height
    def max_height_reached(self, height):
        if height == self.SITTING_HEIGHT:
            return True
        if height == self.STANDING_HEIGHT:
            return True

        return False

    # move the desk up or down depending on the current position
    def toggle_desk(self):
        # TODO: implement logic
        pass

    # returns statzs: UP or DOWN or UNDEFINED
    def deskStatus(self):
        heights = self.getDeskHeight()

        if len(heights) <= 0:
            return "UNDEFINED"

        height = sum(heights) / len(heights)

        if height == self.SITTING_HEIGHT:
            return "DOWN"

        if height == self.STANDING_HEIGHT:
            return "UP"

        return "UNDEFINED"

    # returns a list of measured heights
    def getDeskHeight(self):
        # read current height data and iterate over chunks
        temp = self.converter.split_in_valid_chunks(self.serial.read())
        all_heights = []
        for t in temp:
            height = self.converter.convert_hex_arr_to_number(t)

            # only count valid heights
            if height <= 0:
                continue

            all_heights.append(self.converter.convert_hex_arr_to_number(t))

        return all_heights

    def getCurrentHeight(self):
        rt.gpio_service.enable_write_to_serial()

        gotHeight = True
        while gotHeight:
            rt.serial.activateDesk()
            height = rt.getDeskHeight()

            if height:
                gotHeight = False

        rt.gpio_service.disable_write_to_serial()
        return height


rt = Runntime()

try:
    rt.move_desk("DOWN")
except KeyboardInterrupt:
    pass
finally:
    rt.stop()
