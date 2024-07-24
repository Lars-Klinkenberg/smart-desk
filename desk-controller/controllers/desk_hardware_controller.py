from utils.desk_state import desk_state


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

        if position == "UP":
            pass
        elif position == "DOWN":
            pass

        pass

desk_hardware_controller = DeskHardwareController()
