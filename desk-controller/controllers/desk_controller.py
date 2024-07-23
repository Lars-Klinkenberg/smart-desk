from utils.desk_state import desk_state

class DeskController:
    def move_up(self, increment):
        if desk_state.is_moving:
            return {"error": "Desk is already moving"}
        
        desk_state.start_moving()
        # Simulate the time taken to move the desk (this should be handled by actual hardware logic)
        new_height = desk_state.get_height() + increment
        self._move_physical_desk(new_height)
        desk_state.set_height(new_height)
        desk_state.stop_moving()
        return {"height": new_height}

    def move_down(self, decrement):
        if desk_state.is_moving:
            return {"error": "Desk is already moving"}

        desk_state.start_moving()
        # Simulate the time taken to move the desk (this should be handled by actual hardware logic)
        new_height = desk_state.get_height() - decrement
        self._move_physical_desk(new_height)
        desk_state.set_height(new_height)
        desk_state.stop_moving()
        return {"height": new_height}

    def get_current_height(self):
        return {"height": desk_state.get_height()}

    def _move_physical_desk(self, height):
        # Here should be the logic to physically move the desk
        pass