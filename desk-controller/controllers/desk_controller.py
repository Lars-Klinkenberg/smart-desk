from time import sleep
from utils.desk_state import desk_state
from controllers.desk_hardware_controller import DeskHardwareController

desk_hardware_controller = DeskHardwareController()


class DeskController:
    """
    Controller class for the desk
    """

    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74

    def move(self, direction, iterations=50):
        """
        Moves the desk to the given direction

        Args:
            direction (string): "UP" or "DOWN"
            iterations (int): number of times direction should be written to serial
        """

        if desk_state.is_moving:
            return {"error": "Desk is already moving"}

        desk_state.start_moving()

        for i in range(iterations):
            sleep(0.02)
            desk_hardware_controller.move(direction)

        self.write_default_till_max_reached(direction)

        desk_state.stop_moving()

    def write_default_till_max_reached(self, direction):
        if not desk_state.is_moving:
            return

        while not self.is_max_height_reached(desk_state.get_height(), direction):
            desk_hardware_controller.move("DEFAUKLT")

    def is_max_height_reached(self, height, direction=None) -> bool:
        """
        checks if the height equals the defined standing or sitting height

        Args:
            height (int): the height that should be checked
            direction (string): "UP" or "DOWN" if given check also if right height is reached

        Returns:
            bool: True if height matches STANDING_HEIGHT or SITTING_HEIGHT
        """

        if (height == self.STANDING_HEIGHT) and not (direction == "UP"):
            return True
        if (height == self.SITTING_HEIGHT) and not (direction == "DOWN"):
            return True

        return False

    def get_current_height(self):
        return {"height": desk_state.get_height()}

    def deskStatus(self, height) -> str:
        """
        returns the current status of the desk

        Returns:
            str: UP or DOWN or UNDEFINED
        """

        if height <= 0:
            return "UNDEFINED"

        if height == self.SITTING_HEIGHT:
            return "DOWN"

        if height == self.STANDING_HEIGHT:
            return "UP"

        return "UNDEFINED"

    # returns a list of measured heights
    def getDeskHeight(self, timeout=None):
        # read current height data and iterate over chunks
        temp = self.converter.split_in_valid_chunks(self.serial.read(timeout))
        all_heights = []
        for t in temp:
            height = self.converter.convert_hex_arr_to_number(t)

            # only count valid heights
            if height <= 0:
                continue

            all_heights.append(self.converter.convert_hex_arr_to_number(t))

        return all_heights

    # get the current height even if the desk is not active
    # TODO:  make the function 100% reliable.
    def getCurrentHeight(self, timeout=None) -> int:
        all_heights = self.getDeskHeight(timeout)

        if len(all_heights) <= 0:
            return 0

        height = round(sum(all_heights) / len(all_heights))
        return height

    def handle_moving_request(self, direction):
        if (direction != "UP") and (direction != "DOWN"):
            return False
        
        desk_state.set_moving_direction(direction)
        return True