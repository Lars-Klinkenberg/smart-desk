from time import sleep
from utils.desk_state import desk_state
from utils.serial_service import serial_service


class DeskHardwareController:
    """
    controlls the actual pyhsical desk
    """

    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74

    def move(self, position) -> bool:
        """
        moves the desk to the defined height

        Parameters:
        position (string): "UP" or "DOWN or "DEFAULT"

        Returns:
        bool: True if everything is valid
        """

        print("MOVE ", position)
        # if (position != "UP") and (position != "DOWN") and (position != "DEFAULT"):
        #     return False

        serial_service.write_status(position)
        return True

    def send_move_signal(self, direction, iterations=50):
        """
        Moves the desk to the given direction

        Args:
            direction (string): "UP" or "DOWN"
            iterations (int): number of times direction should be written to serial
        """

        for i in range(iterations):
            sleep(0.01)
            self.move(direction)

    def write_default_till_max_reached(self, direction):
        if not desk_state.is_moving:
            return

        while not self.is_max_height_reached(desk_state.get_height(), direction):
            self.move("DEFAULT")
            sleep(0.03)

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


desk_hardware_controller = DeskHardwareController()
