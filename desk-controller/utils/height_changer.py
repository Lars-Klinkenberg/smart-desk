# app/utils/height_changer.py

from utils.desk_state import desk_state

class HeightChanger:
    def set_height(self, height):
        if desk_state.is_moving:
            return {"error": "Desk is currently moving"}

        desk_state.set_height(height)
        return {"height": desk_state.get_height()}
