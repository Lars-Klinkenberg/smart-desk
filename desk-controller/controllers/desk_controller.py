from time import sleep
from utils.desk_state import desk_state
from controllers.desk_hardware_controller import desk_hardware_controller
from utils.converter_service import converter_service
from utils.serial_service import serial_service
from utils.gpio_service import gpio_service


class DeskController:
    """
    Controller class for the desk
    """

    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74

    def send_move_signal(self, direction, iterations=50):
        """
        Moves the desk to the given direction

        Args:
            direction (string): "UP" or "DOWN"
            iterations (int): number of times direction should be written to serial
        """

        for i in range(iterations):
            sleep(0.02)
            desk_hardware_controller.move(direction)

    def write_default_till_max_reached(self, direction):
        if not desk_state.is_moving:
            return

        while not self.is_max_height_reached(desk_state.get_height(), direction):
            print("Write default")
            desk_hardware_controller.move("DEFAULT")
            sleep(0.02)

    def is_max_height_reached(self, height, direction=None) -> bool:
        """
        checks if the height equals the defined standing or sitting height

        Args:
            height (int): the height that should be checked
            direction (string): "UP" or "DOWN" if given check also if right height is reached

        Returns:
            bool: True if height matches STANDING_HEIGHT or SITTING_HEIGHT
        """

        if (height == self.STANDING_HEIGHT) and (direction == "UP"):
            return True
        if (height == self.SITTING_HEIGHT) and (direction == "DOWN"):
            return True

        return False

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

        if len(all_heights) <= 0:
            return

        height = round(sum(all_heights) / len(all_heights))
        desk_state.set_height(height)
        return height

    def move(self, direction):
        print("MOVING TO:", direction)
        gpio_service.enable_write_to_serial()
        desk_state.start_moving()
        self.send_move_signal(direction, 150)
        self.write_default_till_max_reached(direction)
        gpio_service.disable_write_to_serial()
        desk_state.stop_moving()


desk_controller = DeskController()
