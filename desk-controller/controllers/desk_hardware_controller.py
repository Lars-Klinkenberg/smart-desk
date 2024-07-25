from utils.desk_state import desk_state
from utils.serial_service import serial_service


class DeskHardwareController:
    """
    controlls the actual pyhsical desk
    """

    def move(self, position) -> bool:
        """
        moves the desk to the defined height

        Parameters:
        position (string): "UP" or "DOWN or "DEFAULT"

        Returns:
        bool: True if everything is valid
        """
        if (position != "UP") and (position != "DOWN") and (position != "DEFAULT"):
            return False

        serial_service.write_status(position)
        return True


desk_hardware_controller = DeskHardwareController()
