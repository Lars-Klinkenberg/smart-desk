from time import sleep

from converterService import ConverterService


class DeskController:
    # controller needs more than one short input to react
    # should work with about 15 iterations but sometimes it needs more to react.
    WRITING_ITERATIONS = 50

    # Stop conditions
    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74

    def __init__(self, serialService) -> None:
        self.serial = serialService
        self.converter = ConverterService()

    # moves the desk to the given direction
    # TODO: detect if desk is not moving and handle it
    def move_desk(self, direction):
        print("Moving desk to position: " + direction)

        i = 0
        # send direction signal
        while i != self.WRITING_ITERATIONS:
            i = i + 1
            sleep(0.02)
            self.serial.write_status(direction)

        height = 0
        started_height_adjustment = False

        # write default while height is changing
        while (not self.max_height_reached(height)) and not started_height_adjustment:
            self.serial.write_status("DEFAULT")

            all_heights = self.getDeskHeight()

            if len(all_heights) <= 0:
                continue

            #  get avg of all measured heights
            height = round(sum(all_heights) / len(all_heights))

            # if height is fist time not equal to sitting and standing height
            if (height != self.SITTING_HEIGHT) and (height != self.STANDING_HEIGHT):
                started_height_adjustment = True

        print(f"Moved desk to height: {height}")

    # check if height is equal to sitting or standing height
    def max_height_reached(self, height) -> bool:
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
    def deskStatus(self) -> str:
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

    def getCurrentHeight(self) -> int:

        gotHeight = True
        while gotHeight:
            self.serial.activateDesk()
            height = self.getDeskHeight()

            if height:
                gotHeight = False

        return height
