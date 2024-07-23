from utils.desk_state import desk_state
from controllers.desk_hardware_controller import DeskHardwareController

desk_hardware_controller = DeskHardwareController()

class DeskController:
    STANDING_HEIGHT = 115
    SITTING_HEIGHT = 74

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
        
        
        
        desk_hardware_controller.move()



        
        desk_state.set_height(new_height)
        desk_state.stop_moving()
        return {"height": new_height}

    def get_current_height(self):
        return {"height": desk_state.get_height()}
