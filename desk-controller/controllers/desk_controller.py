from time import sleep
from utils.desk_state import desk_state
from controllers.desk_hardware_controller import desk_hardware_controller
from utils.converter_service import converter_service
from utils.serial_service import serial_service


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

    def desk_status(self, height) -> str:
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

    # returns measured height
    def measure_desk_height(self, timeout=None):
        # read current height data and iterate over chunks
        height_temp = serial_service.read(timeout)
        height_splitted = converter_service.split_in_valid_chunks(height_temp)
        all_heights = []

        for t in height_splitted:
            height = converter_service.convert_hex_arr_to_height(t)

            # only count valid heights
            if height <= 0:
                continue

            all_heights.append(converter_service.convert_hex_arr_to_height(t))

        return round(all_heights.sum() / len(all_heights))

    def handle_moving_request(self, direction):
        if (direction != "UP") and (direction != "DOWN"):
            return False

        desk_state.set_moving_direction(direction)
        return True
