from utils.desk_state import desk_state
from controllers.desk_hardware_controller import DeskHardwareController

desk_hardware_controller = DeskHardwareController()


class DeskController:
    """
    Controller class for the desk
    """

    def move(self, direction):
        """
        Moves the desk to the given direction

        Args:
            direction (string): "UP" or "DOWN"
        """

        if desk_state.is_moving:
            return {"error": "Desk is already moving"}

        return desk_hardware_controller.move(direction)

    def get_current_height(self):
        return {"height": desk_state.get_height()}
