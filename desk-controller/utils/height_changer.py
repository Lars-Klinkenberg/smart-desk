# app/utils/height_changer.py

from utils.desk_state import desk_state


class HeightChanger:
    def set_height(self, height):
        """
        changes the height in the desk state

        Args:
            height (int): current height of the desk

        """

        if height <= 0:
            return {"error": "Height not valid"}

        if desk_state.is_moving:
            return {"error": "Desk is currently moving"}

        desk_state.set_height(height)
        return {"height": desk_state.get_height()}


height_changer = HeightChanger()
