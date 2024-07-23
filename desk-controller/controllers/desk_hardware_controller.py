from utils.desk_state import desk_state


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
        position (string): "UP" or "DOWN

        Returns:
        bool: True if everything is valid
        """

        if position == "UP":
            pass
        elif position == "DOWN":
            pass

        pass

    def is_max_height_reached(self, height) -> bool:
        """
        checks if the height equals the defined standing or sitting height

        Args:
            height (int): the height that should be checked

        Returns:
            bool: True if height matches STANDING_HEIGHT or SITTING_HEIGHT
        """

        if height == self.STANDING_HEIGHT:
            return True
        if height == self.SITTING_HEIGHT:
            return True

        return False
